SCAM_PATTERNS = [
    {
        "type": "冒充公检法诈骗",
        "icon": "👮",
        "keywords": ["公安局", "警察", "民警", "检察院", "检察官", "法院", "法官",
                     "逮捕", "拘留", "冻结账户", "安全账户", "涉嫌洗钱", "配合调查", "通缉", "犯罪"],
        "advice": "公检法机关绝不会通过电话办案，更不会要求转账到所谓\"安全账户\"！请立即挂断电话，拨打110或96110核实。"
    },
    {
        "type": "中奖/领取诈骗",
        "icon": "🎁",
        "keywords": ["中奖", "领取", "奖金", "手续费", "保证金", "先交钱", "验证金",
                     "解冻金", "个人所得税", "公证费"],
        "advice": "正规中奖无需先交任何费用！凡是要求先转账\"手续费\"\"保证金\"才能领奖的，100%是诈骗。"
    },
    {
        "type": "保健品/养老诈骗",
        "icon": "💊",
        "keywords": ["神药", "特效药", "祖传秘方", "免费体验", "健康讲座", "养老理财",
                     "以房养老", "收藏品", "纪念币", "限量发售"],
        "advice": "警惕针对老年人的\"免费体验\"\"健康讲座\"陷阱！建议与子女商量后再决定。"
    },
    {
        "type": "投资理财/杀猪盘",
        "icon": "📈",
        "keywords": ["投资", "理财", "高收益", "稳赚不赔", "内部消息", "导师带单",
                     "杀猪盘", "平台注册", "提现失败", "需充值", "爆仓"],
        "advice": "\"高收益零风险\"不存在！凡是陌生人推荐投资平台、要求充值才能提现的，都是\"杀猪盘\"诈骗。"
    },
    {
        "type": "冒充亲友/紧急求助诈骗",
        "icon": "👤",
        "high_risk": True,
        "keywords": ["急需", "急用", "打钱", "转账", "转点钱", "转钱", "转笔钱", "汇钱", "汇款",
                     "打款", "借钱", "凑钱", "垫付", "换号了", "这是我新号", "在外面不方便",
                     "出事了", "出事", "手术费", "住院", "在医院", "看病", "车祸", "被抓",
                     "病危", "抢救", "保证金", "领导", "张总", "王总"],
        "advice": "收到亲友\"急需用钱\"的消息（尤其\"在医院、出车祸、被抓\"等紧急场景+要求转账），务必先电话或视频核实身份！切勿未经核实就转账。"
    },
    {
        "type": "冒充客服/退款诈骗",
        "icon": "📞",
        "keywords": ["退款", "退货", "客服", "订单异常", "链接", "填写银行卡",
                     "验证码", "快递丢失", "理赔", "取消会员"],
        "advice": "正规退款会原路退回，无需你提供银行卡或验证码！凡是发链接要求填写的，都是诈骗。"
    },
    {
        "type": "贷款/办卡诈骗",
        "icon": "💳",
        "keywords": ["贷款", "无抵押", "秒下款", "额度", "解冻费", "工本费",
                     "包装费", "征信不良", "信用卡办理", "刷流水"],
        "advice": "正规贷款不会要求先交\"解冻费\"\"工本费\"！凡放款前要求先转账的，都是诈骗。"
    },
    {
        "type": "刷单/兼职诈骗",
        "icon": "💼",
        "keywords": ["刷单", "刷信誉", "兼职", "点赞赚钱", "垫付", "返利",
                     "任务", "佣金", "动动手指", "日结"],
        "advice": "\"刷单\"本身违法！凡是要求先垫付资金才能返利的\"兼职\"，都是诈骗。"
    },
]

KNOWLEDGE_BASE = [
    {"icon": "👮", "title": "冒充公检法", "feat": "\"你涉嫌洗钱，把钱转到安全账户\"",
     "body": "骗子冒充公检法，称你涉嫌犯罪，要求将资金转入\"安全账户\"。真相：公检法不会电话办案，更没有\"安全账户\"。"},
    {"icon": "🎁", "title": "中奖诈骗", "feat": "\"恭喜中奖，先交手续费\"",
     "body": "通知你中奖，但领奖前要先交手续费。真相：正规中奖无需先交钱，要求先转账的一律是诈骗。"},
    {"icon": "💊", "title": "保健品诈骗", "feat": "\"免费体验、神药治百病\"",
     "body": "以免费体验、健康讲座为诱饵，推销高价保健品。真相：\"神药\"不存在，购买前务必与子女商量。"},
    {"icon": "📈", "title": "投资理财诈骗", "feat": "\"高收益、稳赚不赔\"",
     "body": "陌生人推荐投资平台，承诺高回报，充值后无法提现。真相：高收益必高风险，\"稳赚不赔\"是骗局。"},
    {"icon": "👤", "title": "冒充亲友", "feat": "\"妈，我出事了，快打钱\"",
     "body": "盗用亲友账号，称出事急需用钱。真相：务必电话/视频核实身份，切勿直接转账。"},
    {"icon": "📞", "title": "客服退款", "feat": "\"订单异常，点链接退款\"",
     "body": "冒充客服，发链接要求填银行卡和验证码。真相：退款原路退回，无需提供验证码。"},
    {"icon": "💳", "title": "贷款诈骗", "feat": "\"无抵押秒下款，先交解冻费\"",
     "body": "称可无抵押贷款，放款前要交解冻费。真相：正规贷款不收前期费用，请找银行办理。"},
    {"icon": "💼", "title": "刷单兼职", "feat": "\"动动手指，日赚几百\"",
     "body": "以刷单兼职为名，要求先垫付资金才能返利。真相：刷单违法，垫付返利都是骗局。"},
]


import re

SUSPICIOUS_SIGNALS = [
    {"cat": "涉及资金", "words": ["转账", "汇款", "打钱", "交钱", "缴费", "充值", "余额", "银行卡", "卡号", "密码", "支付宝", "网银", "取款", "存款", "退款", "返现", "缴纳", "汇入", "转出", "账号"]},
    {"cat": "紧急施压", "words": ["立即", "马上", "赶紧", "尽快", "否则", "后果", "严重", "紧急", "限时", "逾期", "最后", "小时内", "分钟内", "立刻", "务必", "不然"]},
    {"cat": "索要信息", "words": ["验证码", "身份证", "密码", "银行卡号", "手机号", "个人信息", "人脸", "指纹", "短信码", "动态码"]},
    {"cat": "冒充权威", "words": ["公安", "警察", "法院", "政府", "官方", "客服", "工作人员", "主任", "队长", "领导", "总局", "分局", "检察院", "监管", "机构"]},
    {"cat": "引导操作", "words": ["加微信", "加qq", "点击链接", "扫码", "拨打电话", "联系", "添加", "进入", "登录", "填写", "点击", "下载"]},
    {"cat": "诈骗话术", "words": ["安全账户", "清查", "核查", "冻结", "解冻", "注销", "取消", "涉嫌", "违规", "异常", "系统检测", "后台", "洗钱", "犯罪", "立案", "处罚"]},
]


def detect(text: str) -> dict:
    text_lower = text.lower()
    hits = []
    total_kw = 0
    has_high_risk = False
    for pattern in SCAM_PATTERNS:
        matched = [kw for kw in pattern["keywords"] if kw.lower() in text_lower]
        if matched:
            hits.append({
                "type": pattern["type"],
                "icon": pattern["icon"],
                "keywords": matched,
                "advice": pattern["advice"],
            })
            total_kw += len(matched)
            if pattern.get("high_risk"):
                has_high_risk = True

    if not hits:
        sus_cats = []
        sus_words = []
        for s in SUSPICIOUS_SIGNALS:
            matched = [w for w in s["words"] if w in text_lower]
            if matched:
                sus_cats.append(s["cat"])
                sus_words.extend(matched)
        if re.search(r"https?://", text_lower) or "www." in text_lower:
            sus_cats.append("包含链接")
            sus_words.append("网址链接")
        if re.search(r"00\d{6,}", text_lower) or re.search(r"\d{11}", text_lower):
            sus_cats.append("包含电话号码")
            sus_words.append("电话号码")
        if len(sus_cats) >= 3:
            hits.append({
                "type": "可疑信息",
                "icon": "⚠️",
                "keywords": sus_words[:8],
                "advice": "虽然未匹配到已知诈骗类型，但检测到多个可疑特征（%s）。请保持警惕：不轻易转账、不提供个人信息、不点击不明链接。有疑问请拨打 96110 反诈热线咨询。" % "、".join(sus_cats),
            })
            total_kw = len(sus_words)
            level, level_text, level_icon = "mid", "中风险 · 存在可疑特征", "⚠️"
        else:
            level, level_text, level_icon = "low", "未发现诈骗风险", "✅"
    elif (has_high_risk and total_kw >= 2) or len(hits) >= 2 or total_kw >= 4:
        level, level_text, level_icon = "high", "高风险 · 极可能是诈骗", "🚨"
    else:
        level, level_text, level_icon = "mid", "中风险 · 存在诈骗嫌疑", "⚠️"

    return {
        "level": level,
        "level_text": level_text,
        "level_icon": level_icon,
        "hits": hits,
        "total_keywords": total_kw,
        "scam_types": [h["type"] for h in hits],
    }