# 银发守护

前端与后端分开部署：根目录的 `index.html` 是静态前端，`backend/` 是 FastAPI API 服务。后端不再托管前端页面。

## 必须保留

- `index.html`、`frontend-config.js`：前端页面和后端地址配置。
- `backend/main.py`、`backend/detector.py`：API 入口和诈骗检测逻辑。
- `backend/requirements.txt`：后端 Python 依赖。
- `backend/.env.example`：华为云配置模板；部署时复制为 `.env` 并填入真实凭证，不要提交 `.env`。

其他校验脚本和项目材料可按需保留，不影响前后端独立部署。

## 本地运行

在仓库根目录启动后端：

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload
```

用 VS Code Live Server 打开根目录 `index.html`（默认端口 5500），前端会连接 `http://127.0.0.1:8000`。也可在 `frontend-config.js` 中填写 API 地址。

## 分开部署

1. 将根目录 `index.html` 和 `frontend-config.js` 部署到 OBS 静态网站托管或其他静态站点服务。
2. 将 `backend/` 部署到华为云 ECS，安装 `backend/requirements.txt` 后运行：

   ```bash
   uvicorn main:app --app-dir backend --host 0.0.0.0 --port 8000
   ```

3. 把 `frontend-config.js` 中的 `window.SILVER_GUARD_API` 设置为后端 HTTPS 域名；后端 `CORS_ORIGINS` 设置为前端 HTTPS 域名。
4. 在后端环境变量中配置华为云 AK、SK、Project ID 等凭证。仅公开前端和 API 地址，禁止将云凭证写入前端文件。

部署后可访问后端 `/api/health` 检查 API 状态。手机录音需要 HTTPS 页面并允许麦克风权限。