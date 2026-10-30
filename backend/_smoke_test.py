import json
from fastapi.testclient import TestClient
import main

c = TestClient(main.app)

def show(name, resp):
    print("[%s] status=%s" % (name, resp.status_code))
    try:
        body = resp.json()
        print(json.dumps(body, ensure_ascii=False)[:500])
    except Exception as e:
        print("non-json:", resp.text[:300])
    print("-" * 40)

show("health", c.get("/api/health"))
show("knowledge", c.get("/api/knowledge"))
show("patterns", c.get("/api/patterns"))
show("detect/text(high)", c.post("/api/detect/text", json={"text": "我是公安局的，你涉嫌洗钱，请立即将资金转入安全账户配合调查"}))
show("detect/text(empty)", c.post("/api/detect/text", json={"text": "   "}))
show("detect/text(low)", c.post("/api/detect/text", json={"text": "今天天气不错，一起去公园散步吧"}))
show("guard/notify", c.post("/api/guard/notify", json={"level": "high", "scam_types": ["冒充公检法诈骗"], "child_phone": "13800138888", "child_name": "小明"}))