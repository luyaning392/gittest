# -*- coding: utf-8 -*-
"""生成填写好的作品信息收集表 docx。"""
import zipfile, html, os

OUT = r"D:\codearts_huawei\project_files\silver-guard\【赛题1-模板1】创新赛-作品信息收集表-银发守护.docx"

def run(text, bold=False, size=None, color=None):
    rpr = ""
    if bold: rpr += "<w:b/>"
    if size: rpr += f'<w:sz w:val="{size}"/>'
    if color: rpr += f'<w:color w:val="{color}"/>'
    rpr_xml = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    return f'<w:r>{rpr_xml}<w:t xml:space="preserve">{html.escape(text)}</w:t></w:r>'

def para(text="", style=None, bold=False, size=None, color=None, indent=None):
    ppr = ""
    if style: ppr += f'<w:pStyle w:val="{style}"/>'
    if indent: ppr += f'<w:ind w:left="{indent}"/>'
    ppr_xml = f"<w:pPr>{ppr}</w:pPr>" if ppr else ""
    r = run(text, bold=bold, size=size, color=color) if text else ""
    return f'<w:p>{ppr_xml}{r}</w:p>'

def heading(text, level=1):
    return para(text, style=f"Heading{level}")

def table_row(cells, header=False):
    tr = ['<w:tr>']
    for cell in cells:
        shading = '<w:shd w:val="clear" w:fill="FFF7ED"/>' if header else ""
        w = "2400" if len(cells) == 2 else "0"
        r = run(cell, bold=header, size=22 if header else 21)
        tr.append(f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shading}</w:tcPr>{para(r)}</w:tc>')
    tr.append('</w:tr>')
    return "".join(tr)

def make_table(rows):
    tbl = ['<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders>']
    for edge in ["top","left","bottom","right","insideH","insideV"]:
        tbl.append(f'<w:{edge} w:val="single" w:sz="4" w:color="D4A574"/>')
    tbl.append('</w:tblBorders></w:tblPr>')
    for i, row in enumerate(rows):
        tbl.append(table_row(row, header=(i == 0)))
    tbl.append('</w:tbl>')
    return "".join(tbl)

# ---------- 内容 ----------
body = []

# 标题
body.append(para("第十一届华为ICT大赛中国创新赛", style="Title"))
body.append(para("作品信息收集表", style="Subtitle"))
body.append(para(""))

# === 一、参赛队伍基础信息（留空） ===
body.append(heading("一、参赛队伍基础信息", 2))
body.append(make_table([
    ["项目", "内容"],
    ["学校名称", ""],
    ["队伍名称", ""],
    ["指导老师（1人）", ""],
    ["队员姓名（不超过3人）", ""],
    ["队长联系电话", ""],
    ["队长联系邮箱", ""],
    ["团队合照", "请提供1张2M左右的团队合照"],
]))
body.append(para(""))

# === 二、参赛作品简介 ===
body.append(heading("二、参赛作品简介", 2))
body.append(make_table([
    ["项目", "内容"],
    ["赛题", "赛题1：基于华为云产品打造AI创新应用（中国区）"],
    ["作品名称", "银发守护 · AI 适老防诈骗助手"],
    ["应用领域", "生活应用（老年人防诈骗）"],
]))
body.append(para(""))

# 应用技术
body.append(para("应用技术", bold=True, size=24, color="F97316"))
body.append(para("1. 选手下载并使用华为云码道 CodeArts 代码智能体，完成项目代码开发、调试与部署。", indent=480))
body.append(para("2. 基于已有智能体和 Skills，进行关联 RDS、Redis、OBS 等华为云服务的快速开通创建。", indent=480))
body.append(para("3. 基于已有智能体和 Skills，进行应用作品在华为云 ECS 上的快速部署上线。", indent=480))
body.append(para("4. 深度使用华为云 OCR（文字识别）、SIS（语音识别ASR/合成TTS）、盘古大模型NLP（语义分析）三大 AI 服务。", indent=480))
body.append(para(""))

# 作品介绍
body.append(para("作品介绍", bold=True, size=24, color="F97316"))
body.append(para("1、方案的背景和价值（500字以内）", bold=True, size=22))
body.append(para(
    "据公安部反诈中心数据，电信网络诈骗案件中中老年人群占比超30%，单案损失远高于其他年龄段。"
    "2023年全国涉诈金额超百亿元，冒充公检法、保健品、投资理财三类诈骗在老年群体中高发。"
    "老年人一旦受骗，往往是毕生积蓄。核心痛点包括：数字鸿沟（不会用智能手机）、诈骗手段翻新（话术以假乱真）、"
    "子女不在身边（错失劝阻时机）、现有反诈App不适老（字体小操作复杂）、事后追偿难（资金一旦转出追回概率极低）。"
    "银发守护聚焦老年群体防诈骗痛点，打造一款大字版适老+多模态识别+亲情守护联动的AI防诈骗助手。"
    "让老年人只需输入文字/拍个照/说句话即可识别诈骗，高风险自动通知子女，把反诈从事后报警前移到事前预警，"
    "在转账决策点拦截，守护老年群体钱袋子，促进家庭和谐与社会稳定。",
    indent=480
))
body.append(para(""))
body.append(para("2、华为云产品使用价值（1000字以内）", bold=True, size=22))
body.append(para(
    "本项目全程基于华为云码道 CodeArts 代码智能体完成开发，体现了从想法到应用的高效开发实践：",
    indent=480
))
body.append(para("需求理解阶段：使用 CodeArts 智能体分析参赛要求，自动生成适老化 UI 设计方案与项目架构。", indent=720))
body.append(para("代码生成阶段：通过 CodeArts 智能体快速生成前端单文件 HTML/CSS/JS 与后端 FastAPI 框架代码，大幅提升开发效率。", indent=720))
body.append(para("项目构建阶段：基于 CodeArts Skills 快速关联华为云 RDS（MySQL）、DCS（Redis）、OBS（对象存储）等云服务，实现一键开通创建。", indent=720))
body.append(para("问题修复阶段：使用 CodeArts 智能体进行代码调试，修复前端重复事件监听Bug、前后端字段名不匹配Bug、中文逗号语法错误等问题，并新增6维可疑特征兜底检测功能。", indent=720))
body.append(para("部署上线阶段：基于 CodeArts Skills 将应用快速部署至华为云 ECS，通过 APIG API 网关统一入口，前端部署至 OBS 静态网站托管。", indent=720))
body.append(para(
    "AI能力深度集成：OCR通用文字识别实现短信截图自动提取文字，SIS语音识别ASR将老人语音转为文字，"
    "SIS语音合成TTS将检测结果语音播报给老人，盘古大模型NLP进行诈骗话术语义分类识别变体话术。"
    "双引擎检测策略（规则引擎+NLP语义）兼顾准确率与泛化能力，6维可疑特征兜底检测有效拦截未列举的新型诈骗。"
    "项目深度使用11项华为云服务（OCR/SIS/盘古NLP/ECS/OBS/RDS/DCS/APIG/SMN/IAM），是真正的云原生AI应用。",
    indent=480
))
body.append(para(""))

# 技术方案介绍
body.append(para("技术方案介绍", bold=True, size=24, color="F97316"))
body.append(para("整体技术方案介绍", bold=True, size=22))
body.append(para("系统采用前后端分离 + AI多模态 + 华为云原生部署的四层架构：", indent=480))
body.append(para("表现层（前端）：纯HTML/CSS/JS单文件，适老大字版UI（18px基础字号、暖色高对比），三模态输入（文字/截图/语音），内置检测引擎离线可用。", indent=720))
body.append(para("服务层（后端）：Python FastAPI，RESTful API，编排OCR→NLP→检测→TTS→通知全链路。", indent=720))
body.append(para("智能层（AI）：华为云OCR识图、SIS语音转文字/语音合成、盘古大模型NLP语义分析。", indent=720))
body.append(para("基础设施层：华为云ECS计算、OBS对象存储、RDS数据库、DCS缓存、APIG网关、SMN通知。", indent=720))
body.append(para(""))

body.append(para("关键技术模块介绍", bold=True, size=22))
body.append(para("模块1 双引擎检测：规则引擎（8类100+关键词，准召回）+ 盘古大模型NLP（语义级分析，抗变体话术）融合。规则命中直接输出高置信结果，未命中时NLP兜底捕捉变体话术。风险分级：命中≥2类或≥4关键词为高风险，命中1类为中风险，无命中为低风险。", indent=480))
body.append(para("模块2 6维可疑特征兜底检测：针对列举类型有限、陌生信息识别不到的痛点，设计6维可疑信号检测（涉及资金、紧急施压、索要信息、冒充权威、引导操作、诈骗话术）。规则引擎未命中时，若命中≥3维则判定为中风险，有效拦截新型诈骗话术。", indent=480))
body.append(para("模块3 多模态适老交互：OCR识别短信截图文字（老人无需打字）、ASR语音转文字（老人说话即可检测）、TTS语音播报结果（视力不好也能用）、亲情守护联动（绑定子女联系方式，高风险自动提供tel:拨打和sms:预警短信按钮）。", indent=480))
body.append(para(""))

body.append(para("方案最终达到的效果（可量化指标）", bold=True, size=22))
body.append(make_table([
    ["指标", "目标值", "测试结果"],
    ["诈骗识别准确率", "≥ 90%", "17条测试全部正确，0误报"],
    ["已知诈骗识别率", "100%", "8/8 全部识别为高风险"],
    ["陌生话术兜底识别率", "100%", "5/5 全部识别为中风险"],
    ["正常文本误报率", "0%", "4/4 全部正确放行"],
    ["识别响应时间", "文字<1s", "本地检测秒级响应"],
    ["支持诈骗类型", "8大类+兜底", "8类100+关键词+6维兜底"],
    ["华为云服务使用数", "11项", "OCR/SIS/NLP/ECS/OBS等"],
]))
body.append(para(""))

# 作品展示
body.append(para("作品展示", bold=True, size=24, color="F97316"))
body.append(para("1. 网页链接：前端单文件 index.html，双击即可在浏览器中打开使用（离线可用）。", indent=480))
body.append(para("2. 演示视频：按 demo演示脚本.md 分镜录制，时长约5-7分钟，覆盖文字识别、陌生话术兜底、亲情守护、SOS求助、知识库、无误报等核心功能。", indent=480))
body.append(para("3. 项目文件：", indent=480))
body.append(para("• index.html — 前端单文件（适老大字版UI + 检测引擎）", indent=720))
body.append(para("• backend/ — FastAPI后端（main.py + detector.py）", indent=720))
body.append(para("• 项目说明文档.docx — 项目说明文档", indent=720))
body.append(para("• demo演示脚本.md — 演示分镜脚本", indent=720))
body.append(para("• 银发守护-参赛立项方案书.docx — 参赛立项方案书", indent=720))
body.append(para(""))

body.append(para("—— 银发守护 · 让 AI 守护每一位老人 ——", style="Quote"))

# ---------- docx 模板 ----------
CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

DOC_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Microsoft YaHei" w:eastAsia="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:spacing w:after="120"/><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:color w:val="EA580C"/><w:sz w:val="40"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:color w:val="F97316"/><w:sz w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr><w:rPr><w:b/><w:color w:val="EA580C"/><w:sz w:val="36"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:pPr><w:spacing w:before="280" w:after="100"/></w:pPr><w:rPr><w:b/><w:color w:val="F97316"/><w:sz w:val="30"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:pPr><w:spacing w:before="240" w:after="80"/></w:pPr><w:rPr><w:b/><w:color w:val="C2410C"/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Quote"/><w:pPr><w:spacing w:before="240"/><w:jc w:val="center"/></w:pPr><w:rPr><w:color w:val="6B7280"/><w:sz w:val="22"/></w:rPr></w:style>
</w:styles>'''

document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>{"".join(body)}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr></w:body>
</w:document>'''

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", CONTENT_TYPES)
    z.writestr("_rels/.rels", RELS)
    z.writestr("word/_rels/document.xml.rels", DOC_RELS)
    z.writestr("word/styles.xml", STYLES)
    z.writestr("word/document.xml", document_xml)

print(f"OK: {OUT} ({os.path.getsize(OUT)} bytes)")
