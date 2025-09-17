![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/venus-ta-starter/venusta/ci.yml?branch=main)
![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Docker Compose](https://img.shields.io/badge/Docker-Compose-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-informational)
![Vite React](https://img.shields.io/badge/Vite-React-green)

# VenusTA | AI 智能助教系统

完整的**出题 → 评分 → 诊断 → 讲评 → 练习**全流程解决方案，基于Docker化技术栈（FastAPI + Postgres + React+Vite + Nginx）构建。

## 目录

1. [核心能力](#核心能力)
2. [系统架构](#系统架构)
3. [快速启动](#快速启动)
4. [访问地址](#访问地址)
5. [配置说明](#配置说明)
6. [开发工作流](#开发工作流)
7. [测试与冒烟测试](#测试与冒烟测试)
8. [CI/CD集成](#cicd集成)
9. [常见问题排查](#常见问题排查)
10. [项目结构](#项目结构)

## 1. 核心能力

- **智能出题**：基于RAG技术的试题生成，支持配置难度和题型比例
- **AI评分系统**：多裁判LLM评分机制，支持容差设置和自动回退
- **诊断分析**：50+种错误模式识别，生成学生能力画像
- **个性化讲评**：基于表现的针对性复习建议
- **数据看板**：可视化学习指标和进度追踪
- **一键部署**：Docker Compose实现无缝环境搭建
- **全面测试**：内置冒烟测试和全流程验证脚本

## 2. 系统架构

```mermaid
flowchart LR
  subgraph 浏览器
    UI[前端界面 (React+Vite)]
  end

  subgraph Docker容器
    Nginx[Nginx /api反向代理]
    API[FastAPI服务]
    DB[(PostgreSQL数据库 + init.sql)]
  end

  UI -->|/api/*| Nginx -->|HTTP请求| API -->|SQL查询| DB
```

## 3. 快速启动

### 使用批处理脚本（推荐）

直接双击运行以下文件：
- `start_and_test_project.bat` - 完整的项目启动和测试脚本
  - 检查Docker服务状态并尝试启动
  - 启动Docker容器服务
  - 等待服务启动
  - 显示容器状态
  - 测试API连接
  - 提供运行完整API测试的选项
- `run_full_loop.bat` - 仅运行API完整测试的脚本
  - 出题 → 批改 → 诊断 → 讲评 → 看板数据获取

### 使用Docker Compose命令

```bash
# 1) 复制环境变量文件
cp .env.example .env

# 2) 启动服务
 docker compose up -d --build

# 3) 验证安装
curl http://localhost/api/health
# 或打开 http://localhost 和 http://localhost/api/docs
```

### 使用PowerShell命令

```powershell
Start-Service com.docker.service
Copy-Item .env.example .env -Force
docker compose up -d --build
curl http://localhost/api/health -UseBasicParsing
```

## 4. 访问地址

| 服务 | URL | 描述 |
|------|-----|------|
| 前端界面 | [http://localhost](http://localhost) | 主应用界面 |
| API健康检查（代理后） | [http://localhost/api/health](http://localhost/api/health) | 通过Nginx代理的API健康检查 |
| API健康检查（直接） | [http://localhost:8000/health](http://localhost:8000/health) | 直接访问API的健康检查 |
| Swagger文档 | [http://localhost:8000/docs](http://localhost:8000/docs) | 交互式API文档

## 5. 配置说明

在您的`.env`文件中配置以下变量：

| 键 | 示例 | 说明 |
|----|------|------|
| POSTGRES_DB | `venusta` | 数据库名称 |
| POSTGRES_USER | `venusta` | 数据库用户名 |
| POSTGRES_PASSWORD | `venusta` | 数据库密码 |
| POSTGRES_HOST | `db` | Compose服务名称 |
| POSTGRES_PORT | `5432` | 容器内部端口 |
| OPENAI_API_KEY | *(可选)* | 本地开发可留空 |
| OPENAI_BASE_URL | `https://api.openai.com/v1` | 可自定义API端点 |
| EMBEDDING_MODEL | `text-embedding-3-large` | 嵌入模型示例 |
| GENERATION_MODEL | `gpt-4o` | 生成模型示例 |
| SCORING_JUDGE_COUNT | `3` | 多裁判评分数量 |
| SCORING_TOLERANCE | `1` | 评分容差阈值 |

## 6. 开发工作流

### 前端开发优化

前端应用会根据环境自动切换API访问方式：

* **本地开发**：`npm run dev`直接连接`http://localhost:8000`（减少容器重启需求）
* **生产/容器环境**：前端`.env`设置`VITE_API_BASE=/api`，由Nginx去除前缀

**在`src/api.ts`中的实现**：

```ts
const dev = import.meta.env.DEV;
export const API_BASE =
  dev ? "http://localhost:8000" : (import.meta.env.VITE_API_BASE || "/api");
```

## 7. 测试与冒烟测试

### 全流程测试

```bash
# PowerShell
powershell -ExecutionPolicy Bypass -File .\tools\full_loop.ps1 -VerboseLog

# 或
python tools/smoke_test.py

# 或使用批处理脚本
run_full_loop.bat
```

### CI冒烟测试

```bash
python tools/ci_smoke_test.py
```

**测试覆盖内容**：
1. 生成试卷
2. 评分答案
3. 诊断分析
4. 生成讲评
5. 获取仪表板数据

**若测试失败**：检查容器日志
```bash
docker compose logs api
docker compose logs frontend
docker compose logs db
```

## 8. CI/CD集成

### GitHub Actions工作流

- **触发条件**：向`main`分支的`push/pull_request`
- **流程步骤**：
  1. 检出代码
  2. 使用Docker Compose构建
  3. 健康检查服务
  4. 运行冒烟测试
  5. 失败时收集日志
- **生成产物**：`docker logs` / `pytest`报告（如有）

**GitHub Actions配置示例**：

```yaml
# .github/workflows/ci.yml
- name: Smoke Test
  run: |
    pwsh -File tools/full_loop.ps1
```

## 9. 常见问题排查

| 症状 | 检查项 | 解决方案 |
|------|--------|---------|
| `http://localhost/api/health` 返回404 | 检查`nginx.conf`中`proxy_pass`是否有尾部斜杠 | 在`proxy_pass http://api:8000/;`中添加`/`以去除前缀 |
| API无法连接数据库 | `docker compose logs api`, `db` | 核对`.env`中的`POSTGRES_*`设置；首次启动检查`init.sql`是否执行 |
| 前端调用API报CORS/路径错误 | 检查`.env`中`VITE_API_BASE`是否为`/api` | 本地开发直连8000端口，生产环境使用代理 |
| 端口占用 | `netstat -ano` | 修改compose映射或释放占用的端口 |
| Edge浏览器触发Bing搜索错误 | 浏览器地址栏行为 | 输入完整URL或使用批处理脚本；在Edge设置中禁用"使用Bing搜索输入内容"选项 |
| 网络连接问题 | 当前网络环境 | ✅ 国内网站访问正常；❌ 部分国外网站受限；✅ Bing域名解析正常；❌ Bing连接可能被拦截

## 10. 项目结构

```
services/
├── .env                  # 环境变量配置文件
├── .env.example          # 环境变量示例文件
├── .github/workflows/ci.yml  # GitHub Actions CI配置
├── api/                  # 后端API服务
│   ├── Dockerfile        # API服务Docker配置
│   ├── app/              # 后端应用代码
│   │   ├── main.py       # API入口文件
│   │   ├── routers/      # API路由
│   │   ├── db.py         # 数据库连接
│   │   └── tests/        # 后端测试
│   └── scripts/          # 后端脚本
│       └── seed_questions.py # 题库初始化脚本
├── db/                   # 数据库初始化脚本
├── docker-compose.yml    # Docker Compose配置
├── run_full_loop.bat     # 一键API测试脚本
├── start_and_test_project.bat # 启动和测试项目脚本
├── tools/                # 测试和工具脚本
│   ├── ci_smoke_test.py  # CI环境冒烟测试
│   ├── full_loop.ps1     # 完整测试流程
│   └── smoke_test.py     # 冒烟测试
└── venusta-frontend/     # 前端React应用
    ├── .env              # 前端环境变量
    ├── Dockerfile        # 前端Docker配置
    ├── nginx.conf        # Nginx配置
    ├── package.json      # 前端依赖
    └── src/              # 前端源码
        ├── App.tsx       # 主应用组件
        ├── api.ts        # API调用封装
        └── main.tsx      # 入口文件
```

## 演示/路演准备

如需进行项目演示，建议提前准备：

1. **初始化种子数据**
   ```powershell
   python .\api\scripts\seed_questions.py
   ```

2. **使用完整测试脚本预热系统**
   ```powershell
   .\run_full_loop.bat
   ```

3. **检查所有服务状态**
   ```powershell
   docker compose ps
   ```

4. **确保网络连接稳定**
   由于部分国外服务可能受限，请确保演示环境网络连接稳定。

## 许可证

本项目采用 MIT 许可证。

## 联系方式

如有任何问题或需要进一步的帮助，请联系项目团队。