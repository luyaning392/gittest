import os
import base64
import logging
from typing import Literal, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from detector import detect, KNOWLEDGE_BASE, SCAM_PATTERNS

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("silver-guard")

app = FastAPI(
    title="银发守护 · AI 防诈骗助手 API",
    description="基于华为云盘古大模型/OCR/语音识别的适老化防诈骗服务",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AK = os.getenv("HUAWEI_AK", "")
SK = os.getenv("HUAWEI_SK", "")
REGION = os.getenv("HUAWEI_REGION", "cn-north-4")
PROJECT_ID = os.getenv("HUAWEI_PROJECT_ID", "")
OBS_BUCKET = os.getenv("OBS_BUCKET", "silver-guard-assets")
PANGU_MODEL_ID = os.getenv("PANGU_MODEL_ID", "")
ASR_MODELS = {
    "mandarin": "chinese_16k_general",
    "sichuan": "sichuan_16k_common",
    "cantonese": "cantonese_16k_common",
    "shanghai": "shanghai_16k_common",
}


def _has_credentials() -> bool:
    values = (AK, SK, PROJECT_ID)
    placeholders = ("your-", "your_", "<", "${")
    return all(value.strip() and not value.strip().lower().startswith(placeholders) for value in values)


def ocr_recognize(image_base64: str) -> str:
    if not _has_credentials():
        logger.warning("华为云凭证未配置，OCR 返回空")
        return ""
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        try:
            from huaweicloudsdkocr.v1 import OcrClient
            from huaweicloudsdkocr.v1.region.ocr_region import OcrRegion
            from huaweicloudsdkocr.v1.model import (
                RecognizeGeneralTextRequest,
                GeneralTextRequestBody,
            )
        except ImportError:
            from huaweicloudsdkocr import OcrClient
            from huaweicloudsdkocr.v2.region.ocr_region import OcrRegion
            from huaweicloudsdkocr.v2 import (
                RecognizeGeneralTextRequest,
                GeneralTextRequestBody,
            )

        credentials = BasicCredentials() \
            .with_ak(AK).with_sk(SK).with_project_id(PROJECT_ID)
        client = OcrClient.new_builder().with_credentials(credentials).with_region(OcrRegion.value_of(REGION)).build()

        body = GeneralTextRequestBody(image=image_base64)
        request = RecognizeGeneralTextRequest(body=body)
        response = client.recognize_general_text(request)

        words = []
        for block in response.result.words_block_list:
            words.append(block.words)
        return "".join(words)
    except Exception as e:
        logger.error("OCR 调用失败: %s", e)
        return ""


def nlp_enhance_detect(text: str, base_result: dict) -> dict:
    if not _has_credentials() or not PANGU_MODEL_ID:
        return base_result
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdknlp import NlpClient
        from huaweicloudsdknlp.v1 import (
            RunTextClassificationRequest,
            TextClassificationReq,
        )

        credentials = BasicCredentials() \
            .with_ak(AK).with_sk(SK).with_project_id(PROJECT_ID)
        client = NlpClient.new_builder().with_credentials(credentials).with_region(REGION).build()

        req = TextClassificationReq(text=text, model_id=PANGU_MODEL_ID)
        request = RunTextClassificationRequest(body=req)
        response = client.run_text_classification(request)

        if response.result:
            label = response.result.label
            confidence = getattr(response.result, "confidence", 0)
            if label and "诈骗" in str(label):
                if base_result["level"] == "low":
                    base_result["level"] = "mid"
                    base_result["level_text"] = "中风险 · AI模型识别到诈骗嫌疑"
                    base_result["level_icon"] = "⚠️"
                base_result["ai_model"] = {
                    "label": label,
                    "confidence": round(confidence, 4),
                }
    except Exception as e:
        logger.error("NLP 盘古大模型调用失败: %s", e)
    return base_result


def asr_recognize(audio_base64: str, dialect: str = "mandarin") -> tuple[str, Optional[float]]:
    if not _has_credentials():
        logger.warning("华为云凭证未配置，ASR 返回空")
        return ""
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        try:
            from huaweicloudsdksis.v1 import SisClient
            from huaweicloudsdksis.v1.region.sis_region import SisRegion
            from huaweicloudsdksis.v1.model import (
                Config,
                RecognizeShortAudioRequest,
                PostShortAudioReq,
            )
        except ImportError:
            from huaweicloudsdksis import SisClient
            from huaweicloudsdksis.v1.region.sis_region import SisRegion
            from huaweicloudsdksis.v1 import (
                RecognizeShortAudioRequest,
                PostShortAudioReq,
            )
            Config = None

        credentials = BasicCredentials() \
            .with_ak(AK).with_sk(SK).with_project_id(PROJECT_ID)
        client = SisClient.new_builder().with_credentials(credentials).with_region(SisRegion.value_of(REGION)).build()

        model_property = ASR_MODELS.get(dialect, ASR_MODELS["mandarin"])
        if "config" in PostShortAudioReq.openapi_types:
            config = Config(
                audio_format="wav",
                _property=model_property,
                add_punc="yes",
            )
            body = PostShortAudioReq(data=audio_base64, config=config)
        else:
            body = PostShortAudioReq(
                data=audio_base64,
                audio_format="wav",
                model_property=model_property,
                add_punctuation=True,
            )
        request = RecognizeShortAudioRequest(body=body)
        response = client.recognize_short_audio(request)

        if not response.result:
            return "", None
        return response.result.text or "", getattr(response.result, "score", None)
    except Exception as e:
        logger.error("ASR 语音识别失败: %s", e)
        return "", None


def tts_synthesize(text: str) -> Optional[str]:
    if not _has_credentials():
        return None
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        try:
            from huaweicloudsdksis.v1 import SisClient, RunTtsRequest
            from huaweicloudsdksis.v1.region.sis_region import SisRegion
            from huaweicloudsdksis.v1.model import PostCustomTTSReq, TtsConfig
            PostTtsReq = None
        except ImportError:
            from huaweicloudsdksis import SisClient
            from huaweicloudsdksis.v1 import RunTtsRequest, PostTtsReq
            from huaweicloudsdksis.v1.region.sis_region import SisRegion
            PostCustomTTSReq = None
            TtsConfig = None

        credentials = BasicCredentials() \
            .with_ak(AK).with_sk(SK).with_project_id(PROJECT_ID)
        client = SisClient.new_builder().with_credentials(credentials).with_region(SisRegion.value_of(REGION)).build()

        if PostCustomTTSReq:
            config = TtsConfig(
                audio_format="wav",
                sample_rate="16000",
                _property="chinese_xiaoyan_common",
            )
            body = PostCustomTTSReq(text=text, config=config)
        else:
            body = PostTtsReq(text=text, audio_format="wav", sample_rate=16000, voice="xiaoyan")
        request = RunTtsRequest(body=body)
        response = client.run_tts(request)

        if not response.result:
            return None
        return getattr(response.result, "data", None) or getattr(response.result, "audio", None)
    except Exception as e:
        logger.error("TTS 语音合成失败: %s", e)
        return None


def obs_upload(key: str, data: bytes) -> Optional[str]:
    if not _has_credentials():
        return None
    try:
        from obs import ObsClient

        obs = ObsClient(access_key_id=AK, secret_access_key=SK, server=os.getenv("OBS_ENDPOINT", ""))
        resp = obs.putContent(OBS_BUCKET, key, data)
        if resp.status < 300:
            return f"https://{OBS_BUCKET}.{os.getenv('OBS_ENDPOINT','')}/{key}"
        return None
    except Exception as e:
        logger.error("OBS 上传失败: %s", e)
        return None


class TextDetectRequest(BaseModel):
    text: str


class VoiceDetectRequest(BaseModel):
    audio_base64: str
    dialect: Literal["mandarin", "sichuan", "cantonese", "shanghai"] = "mandarin"


class GuardNotifyRequest(BaseModel):
    level: str
    scam_types: list
    child_phone: str
    child_name: Optional[str] = ""


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "silver-guard", "cloud_ready": _has_credentials()}


@app.get("/api/knowledge")
def knowledge():
    return {"items": KNOWLEDGE_BASE, "total": len(KNOWLEDGE_BASE)}


@app.get("/api/patterns")
def patterns():
    return {
        "patterns": [
            {"type": p["type"], "icon": p["icon"], "keyword_count": len(p["keywords"])}
            for p in SCAM_PATTERNS
        ],
        "total_types": len(SCAM_PATTERNS),
    }


@app.post("/api/detect/text")
def detect_text(req: TextDetectRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text 不能为空")
    result = detect(req.text)
    result = nlp_enhance_detect(req.text, result)
    result["input_length"] = len(req.text)
    logger.info("文字检测完成 level=%s types=%s", result["level"], result.get("scam_types"))
    return result


@app.post("/api/detect/sms")
async def detect_sms(file: UploadFile = File(...)):
    if not _has_credentials():
        raise HTTPException(
            status_code=503,
            detail="未配置真实华为云凭证。请在 backend/.env 中填写 HUAWEI_AK、HUAWEI_SK 和 HUAWEI_PROJECT_ID。",
        )
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="图片为空")
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    obs_url = obs_upload(f"sms/{file.filename}", image_bytes)

    ocr_text = ocr_recognize(image_b64)
    if not ocr_text:
        raise HTTPException(
            status_code=502,
            detail="华为云 OCR 调用失败或未识别到文字，请检查图片格式、OCR 服务权限及后端日志。",
        )

    result = detect(ocr_text)
    result = nlp_enhance_detect(ocr_text, result)
    result["ocr_text"] = ocr_text
    result["obs_url"] = obs_url
    logger.info("短信截图检测完成 level=%s", result["level"])
    return result


@app.post("/api/detect/voice")
def detect_voice(req: VoiceDetectRequest):
    if not _has_credentials():
        raise HTTPException(
            status_code=503,
            detail="未配置真实华为云凭证。请在 backend/.env 中填写 HUAWEI_AK、HUAWEI_SK 和 HUAWEI_PROJECT_ID。",
        )
    if not req.audio_base64:
        raise HTTPException(status_code=400, detail="audio_base64 不能为空")
    if req.dialect != "mandarin" and REGION != "cn-north-4":
        raise HTTPException(
            status_code=400,
            detail="当前方言模型仅支持 cn-north-4 区域，请调整 backend/.env 中的 HUAWEI_REGION。",
        )

    asr_text, asr_confidence = asr_recognize(req.audio_base64, req.dialect)
    if not asr_text:
        raise HTTPException(
            status_code=502,
            detail="华为云 SIS 调用失败或未识别到语音，请检查服务权限、区域、音频格式及后端日志。",
        )

    result = detect(asr_text)
    result = nlp_enhance_detect(asr_text, result)
    result["asr_text"] = asr_text
    result["asr_confidence"] = asr_confidence

    if result["level"] in ("mid", "high"):
        tts_audio = tts_synthesize(result["level_text"] + "，请立即停止操作并联系子女。")
        if tts_audio:
            result["tts_audio"] = tts_audio

    logger.info("语音检测完成 level=%s", result["level"])
    return result


@app.post("/api/guard/notify")
def guard_notify(req: GuardNotifyRequest):
    if req.level != "high":
        return {"sent": False, "reason": "仅高风险触发通知"}

    logger.warning(
        "【亲情守护预警】向 %s(%s) 发送预警：检测到高风险诈骗 %s",
        req.child_name or "子女",
        req.child_phone,
        req.scam_types,
    )
    return {
        "sent": True,
        "to": req.child_phone,
        "name": req.child_name,
        "scam_types": req.scam_types,
        "message": f"【银发守护预警】检测到高风险诈骗：{','.join(req.scam_types)}，请尽快联系父母确认！",
    }


@app.post("/api/tts")
def tts(req: TextDetectRequest):
    audio = tts_synthesize(req.text)
    if not audio:
        raise HTTPException(status_code=500, detail="语音合成失败")
    return {"audio_base64": audio, "format": "wav"}


# ============ 静态前端托管（让 FastAPI 同时服务前端页面） ============
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

_static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.isdir(_static_dir):
    app.mount("/static", StaticFiles(directory=_static_dir), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(_static_dir, "index.html"))


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    logger.info("银发守护 API 启动 %s:%s 云服务就绪=%s", host, port, _has_credentials())
    uvicorn.run(app, host=host, port=port)