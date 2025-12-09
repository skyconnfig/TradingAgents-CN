# TradingAgents-CN Windows 系统部署指南

面向 Windows 10/11 64 位环境，指导在本机部署并运行整套系统（前端 Vue、后端 FastAPI、数据库 MongoDB/Redis）。文档包含依赖准备、环境变量、构建与启动、集成验证、故障排查与日志位置说明。

---

## 1. 环境准备要求

- 操作系统：Windows 10/11 64 位，建议启用 PowerShell 7 或 Windows Terminal
- 必备软件及版本：
  - Python `>= 3.10`（项目声明 `pyproject.toml` 要求，见 `pyproject.toml:10`）
  - Node.js `>= 18.0.0`（前端 `frontend/package.json:55-58`）
  - 包管理器：Yarn（推荐）或 npm（均可）
  - Git（用于代码获取与版本管理）
  - MongoDB 数据库（建议 4.4+；Compose 使用镜像 `mongo:4.4`，见 `docker-compose.yml:96-103`）
  - Redis 缓存（建议 7.x；Compose 使用 `redis:7-alpine`，见 `docker-compose.yml:126-133`）
  - 可选：wkhtmltopdf（若启用 PDF 导出，后端依赖 `pdfkit`，见 `pyproject.toml:71-76`）

- 系统环境变量（如使用代理访问国外模型服务）：
  - `HTTP_PROXY`、`HTTPS_PROXY`（可选）
  - `NO_PROXY=localhost,127.0.0.1,eastmoney.com,...`（避免国内数据源走代理，示例见 `.env.example:44-53` 与 `app/core/config.py:109-113`）

---

## 2. 前端部署步骤（Vue + Vite）

- 依赖安装（推荐 Yarn）：

```powershell
cd frontend
corepack enable  # 若首次使用 Yarn
yarn install --frozen-lockfile
# 如使用 npm：npm install
```

- 开发环境配置（可选）：
  - 开发模式已在 `vite.config.ts:42-59` 配置了 `server.port=3000` 与 `/api` 代理至后端 `http://localhost:8000`（含 WebSocket）。因此开发模式可不设置 `VITE_API_BASE_URL`。
  - 生产模式需设置后端地址：在 `frontend/.env.production` 写入：

```env
VITE_API_BASE_URL=http://localhost:8000
```

- 构建命令：

```powershell
# 标准构建（含类型检查）
yarn build  # 等价于：vue-tsc && vite build

# 快速构建（跳过类型检查，脚本中用于便携包）：
yarn vite build
```

- 启动方式：
  - 开发模式（端口 3000）：

```powershell
yarn dev  # 访问 http://localhost:3000
```

  - 生产模式（两种方式）：
    - 方式 A：Vite 预览服务

```powershell
yarn preview --port 4173  # 访问 http://localhost:4173
```

    - 方式 B：Nginx 静态服务 + 反向代理（推荐生产）
      - 将 `frontend/dist` 作为静态目录；`/api/` 代理到后端 `http://localhost:8000` 并开启 WebSocket。
      - 参考 Compose 的 Nginx 配置 `nginx/nginx.conf:51-84`，将 `backend` 与 `frontend` 主机名替换为本机地址。

---

## 3. 后端部署步骤（Python + FastAPI）

- 创建并激活虚拟环境：

```powershell
cd d:\daima\TradingAgents-CN
python -m venv .venv
.\.venv\Scripts\activate
```

- 安装依赖：

```powershell
# 推荐（开发）：可编辑安装，复用 pyproject 依赖
pip install -e .

# 备选：使用 requirements.txt（已标记弃用，仍可用）
pip install -r requirements.txt
```

- 应用配置文件：
  - 复制 `.env.example` → `.env`，并至少配置以下项（后端默认读取 `.env`，见 `app/core/config.py:285-288`）：

```env
# 基础服务
DEBUG=true
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=["http://localhost:3000"]

# MongoDB（开发可不启用认证：留空 USERNAME/PASSWORD）
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USERNAME=
MONGODB_PASSWORD=
MONGODB_DATABASE=tradingagents
MONGODB_AUTH_SOURCE=admin

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# 安全（必须为随机值，生产务必修改）
JWT_SECRET=<使用 python 生成>
CSRF_SECRET=<使用 python 生成>
```

  - 生成强随机密钥：

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

- 服务启动命令与端口：
  - 推荐命令：

```powershell
# 读取 settings 并运行 uvicorn（含 reload 取决于 DEBUG）
python -m app
```

    - 该入口位于 `app/__main__.py:166-171`，后端应用定义于 `app/main.py`，标准 uvicorn 启动位于 `app/main.py:745-764`。

  - 备选命令：

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- 端口与跨域：
  - 后端默认端口 `8000`（见 `app/core/config.py:24-27`）
  - 前端开发端口 `3000`（见 `frontend/vite.config.ts:42-45`）
  - `ALLOWED_ORIGINS` 需包含前端来源，否则浏览器跨域请求会被拒绝（见 `app/main.py:621-627`）

---

## 4. 数据库部署

- MongoDB 安装与启动（本机）：
  - 下载安装 MongoDB Community（Windows）；安装后启动 `mongod` 服务（默认端口 27017）
  - 开发环境建议关闭认证或创建账号后在 `.env` 配置用户名密码
  - 初始化集合与索引（可选）：如需快速插入基础集合与示例数据，可使用项目提供的初始化脚本：

```powershell
# 使用 mongo shell 执行初始化（需将路径替换为实际安装路径）
mongo localhost:27017/tradingagents < scripts\docker\mongo-init.js
```

  - 参考初始化脚本内容与索引：见 `scripts/docker/mongo-init.js:7-15,18-25,27-35`

- Redis 安装与启动（本机）：
  - 下载安装 Redis for Windows（或使用 WSL/容器版），启动 `redis-server.exe`（默认端口 6379）
  - 若设置了 `REDIS_PASSWORD`，需在启动参数中启用 `--requirepass <password>`（与 Compose 一致，见 `docker-compose.yml:132-135`）

- 连接字符串配置：
  - MongoDB：后端按 `MONGODB_*` 构建 URI（见 `app/core/config.py:44-51`）
  - Redis：后端按 `REDIS_*` 构建 URL（见 `app/core/config.py:65-71`）

- 权限设置要求：
  - 开发环境可无鉴权运行（本机），生产必须启用数据库账号并使用强密码
  - 若启用 MongoDB 认证，确保 `MONGODB_AUTH_SOURCE=admin` 与对应用户存在

---

## 5. 系统集成验证

- 各组件启动顺序：
  - 1) 启动 MongoDB 与 Redis → 2) 启动后端 → 3) 启动前端

- 服务健康检查：

```powershell
# 后端健康
curl http://localhost:8000/api/health
# 后端测试日志端点（含请求日志）
curl http://localhost:8000/api/test-log
# 前端开发页面
start http://localhost:3000
```

- 功能与环境验证脚本：

```powershell
# 运行项目内安装验证脚本
ython examples\test_installation.py
```

- 常见问题排查：
  - 端口占用：

```powershell
# 查看端口占用（示例：8000/3000/27017/6379）
netstat -ano | findstr :8000
netstat -ano | findstr :3000
netstat -ano | findstr :27017
netstat -ano | findstr :6379
```

  - 跨域错误：确保后端 `ALLOWED_ORIGINS` 包含前端地址（见 `app/main.py:621-627`）
  - 认证失败：确认 `JWT_SECRET` 和 `CSRF_SECRET` 已设置且后端已重启
  - 数据库连接失败：检查服务是否启动、防火墙放行端口、用户名密码是否匹配
  - 国内数据源请求超时：检查代理设置并配置 `NO_PROXY`（见 `.env.example:44-53`）
  - PDF 导出失败：安装 wkhtmltopdf 并将可执行文件加入 `PATH`

- 日志文件位置：
  - 后端：`logs/tradingagents.log`（默认配置，见 `.env.example:490-493` 与 `app/core/config.py:100-103`）
  - Nginx（如使用）：参考安装目录 `logs/` 或自定义路径
  - 前端开发：控制台输出（浏览器与终端）；生产由 Web 服务器日志记录

---

## 6. 生产部署建议（可选）

- 反向代理：使用 Nginx 统一入口，静态页面与 `/api` 代理不同上游；参考 `nginx/nginx.conf:51-84`
- 进程管理：后端建议使用 `pm2`（Node 版 uvicorn 管理不适用）或 NSSM/Windows 服务方式维持长期运行
- 安全性：生产禁用 `DEBUG`、设置强密钥与数据库密码、限制 `HOST` 为内网地址并在防火墙开放必要端口

---

## 7. 附录：Docker Compose 快速启动（可选）

如需快速体验，项目提供一键容器化方案（包含后端、前端、MongoDB/Redis）：

```powershell
# 在项目根目录执行
docker compose up -d
# 访问地址
echo API: http://localhost:8000
start http://localhost:3000
```

- 端口映射与环境变量参考：`docker-compose.yml:15-43,71-88,100-148`
- 容器健康检查与启动顺序：见 `docker-compose.yml:44-56,82-88,111-118,138-144`

---

## 8. 账号初始化（可选）

如需创建默认管理员账号用于前端登录（开发环境）：

```powershell
# 默认 admin/admin123（可带参数覆盖）
python scripts\create_default_admin.py --overwrite
```

- 脚本细节与连接字符串：见 `scripts/create_default_admin.py:29-33,149-167,200-247`

---

以上步骤完成后，即可在 Windows 本机完整运行 TradingAgents-CN 的前端、后端与数据库组件。若遇到问题，请先检查日志与健康端点，再按故障排查清单逐项定位并修复。