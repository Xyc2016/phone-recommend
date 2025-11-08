# 手机推荐 AI Agent - 后端

## 技术栈

- **FastAPI** - 异步 Web 框架
- **Motor** - MongoDB 异步驱动
- **LangChain** - LLM 应用框架
- **OpenAI** - AI 模型
- **SSE** - Server-Sent Events 流式响应
- **uv** - Python 包和虚拟环境管理

## 项目结构

```
be/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── thread.py
│   │   └── message.py
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py
│   │   ├── chat_service.py  # 对话服务
│   │   └── llm_service.py   # LLM 服务
│   └── api/                 # API 路由
│       ├── __init__.py
│       ├── threads.py       # 对话线程 API
│       └── messages.py      # 消息 API
├── pyproject.toml           # uv 项目配置
├── uv.lock (自动生成，可选)
├── .env.example
└── README.md
```

## 环境设置（使用 [uv](https://github.com/astral-sh/uv)）

### 1. 安装 uv（若尚未安装）

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# 或参考官方文档安装
```

### 2. 安装依赖并创建虚拟环境

```bash
cd be
uv sync
```

该命令会自动创建 `.venv` 虚拟环境并安装 `pyproject.toml` 中声明的依赖。

### 3. 激活虚拟环境

```bash
uv venv --activate
# 或者使用 shell hook:
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate    # Windows
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 OpenAI API Key 和 MongoDB 连接信息
```

### 5. 启动 MongoDB

确保 MongoDB 服务正在运行：

```bash
# 使用 Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# 或使用本地安装的 MongoDB
mongod
```

### 6. 启动开发服务器

```bash
uv run dev
# 或
uv run start
```

## API 文档

启动服务器后，访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 端点

### 对话线程

- `GET /api/threads` - 获取所有对话线程
- `POST /api/threads` - 创建新对话线程
- `GET /api/threads/{thread_id}` - 获取单个对话线程
- `DELETE /api/threads/{thread_id}` - 删除对话线程

### 消息

- `POST /api/threads/{thread_id}/messages` - 发送消息（SSE 流式响应）
- `GET /api/threads/{thread_id}/messages` - 获取对话消息列表

## 环境变量说明

- `OPENAI_API_KEY`: OpenAI API 密钥（必需）
- `OPENAI_MODEL`: 使用的 OpenAI 模型（默认: gpt-4-turbo-preview）
- `MONGODB_URL`: MongoDB 连接 URL（默认: mongodb://localhost:27017）
- `MONGODB_DB_NAME`: 数据库名称（默认: phone_recommend）
- `HOST`: 服务器主机（默认: 0.0.0.0）
- `PORT`: 服务器端口（默认: 8000）
- `CORS_ORIGINS`: CORS 允许的源（逗号分隔）

