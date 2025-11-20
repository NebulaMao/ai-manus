# AI Manus 源码结构

## 📋 文档信息

| 属性 | 值 |
|------|-----|
| **项目名称** | AI Manus - 通用AI Agent系统 |
| **结构版本** | v1.0 |
| **创建日期** | 2025-11-05 |
| **适用范围** | 全项目源码组织 |
| **架构类型** | Monorepo + 微服务 |

---

## 🚀 项目结构概览

AI Manus 采用 Monorepo 结构管理多个微服务模块，每个模块职责明确，边界清晰。整体结构遵循领域驱动设计(DDD)原则，便于团队协作和项目维护。

### 整体目录结构

```
ai-manus/
├── .github/                    # GitHub Actions 配置
├── .bmad-core/                 # BMad 框架配置
├── docs/                       # 项目文档
├── frontend/                   # 前端应用
├── backend/                    # 后端 API 服务
├── sandbox/                    # 沙箱环境服务
├── mockserver/                 # 开发模拟服务
├── scripts/                    # 构建和部署脚本
├── tests/                      # 集成测试
├── .env.example               # 环境变量模板
├── .gitignore                 # Git 忽略文件
├── docker-compose.yml         # 开发环境编排
├── docker-compose.prod.yml    # 生产环境编排
├── README.md                  # 项目说明
└── CLAUDE.md                  # AI 助手上下文
```

---

## 📁 根级文件详解

### 配置文件

#### `.gitignore`
```gitignore
# 依赖目录
node_modules/
__pycache__/
*.pyc
.pytest_cache/

# 环境配置
.env
.env.local
.env.production

# 构建输出
dist/
build/
.coverage
htmlcov/

# IDE 文件
.vscode/
.idea/
*.swp
*.swo

# 日志文件
*.log
logs/

# 临时文件
tmp/
temp/
.DS_Store
Thumbs.db

# Docker
.dockerignore

# BMad 框架
.bmad-core/cache/
.bmad-core/logs/
```

#### `docker-compose.yml`
```yaml
version: '3.8'

services:
  # 前端开发服务
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_BASE_URL=http://localhost:8000
      - VITE_WS_URL=ws://localhost:8000
    depends_on:
      - backend

  # 后端 API 服务
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - MONGODB_URL=mongodb://mongodb:27017/ai_manus
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=true
    depends_on:
      - mongodb
      - redis

  # 沙箱服务
  sandbox:
    build:
      context: ./sandbox
      dockerfile: Dockerfile.dev
    ports:
      - "8080:8080"
      - "5900:5900"  # VNC 端口
    volumes:
      - ./sandbox:/app
    environment:
      - DOCKER_HOST=unix:///var/run/docker.sock
    privileged: true

  # 模拟服务
  mockserver:
    build:
      context: ./mockserver
      dockerfile: Dockerfile.dev
    ports:
      - "9000:9000"
    volumes:
      - ./mockserver:/app

  # 数据库服务
  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_DATABASE=ai_manus

  # 缓存服务
  redis:
    image: redis:7.0-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  mongodb_data:
  redis_data:
```

#### `.env.example`
```bash
# 应用配置
APP_NAME=AI Manus
APP_VERSION=1.0.0
DEBUG=false
ENVIRONMENT=development

# 数据库配置
MONGODB_URL=mongodb://localhost:27017/ai_manus
REDIS_URL=redis://localhost:6379/0

# 安全配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM 配置
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-3.5-turbo
MAX_TOKENS=2048
TEMPERATURE=0.7

# Docker 配置
DOCKER_HOST=unix:///var/run/docker.sock
SANDBOX_NETWORK=ai-manus-sandbox
VNC_PASSWORD=vnc123

# 搜索配置
SEARCH_PROVIDER=bing
BING_API_KEY=your-bing-api-key
GOOGLE_API_KEY=your-google-api-key
BAIDU_API_KEY=your-baidu-api-key

# 前端配置
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_VNC_URL=ws://localhost:5900

# 监控配置
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
```

---

## 🖥️ Frontend 目录结构

### 完整目录树

```
frontend/
├── public/                     # 静态资源
│   ├── favicon.ico
│   ├── logo.svg
│   └── index.html
├── src/                        # 源代码
│   ├── api/                    # API 客户端
│   │   ├── index.ts           # API 配置
│   │   ├── auth.ts            # 认证 API
│   │   ├── agents.ts          # Agent API
│   │   ├── tasks.ts           # 任务 API
│   │   └── websocket.ts       # WebSocket 客户端
│   ├── assets/                # 静态资源
│   │   ├── images/
│   │   ├── icons/
│   │   └── styles/
│   ├── components/            # 组件库
│   │   ├── common/           # 通用组件
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppSidebar.vue
│   │   │   ├── AppFooter.vue
│   │   │   ├── LoadingSpinner.vue
│   │   │   ├── ErrorMessage.vue
│   │   │   └── ConfirmDialog.vue
│   │   ├── forms/            # 表单组件
│   │   │   ├── LoginForm.vue
│   │   │   ├── AgentForm.vue
│   │   │   ├── TaskForm.vue
│   │   │   └── UserForm.vue
│   │   ├── layout/           # 布局组件
│   │   │   ├── DefaultLayout.vue
│   │   │   ├── AuthLayout.vue
│   │   │   └── DashboardLayout.vue
│   │   └── ui/               # UI 基础组件
│   │       ├── Button.vue
│   │       ├── Input.vue
│   │       ├── Modal.vue
│   │       ├── Card.vue
│   │       └── Table.vue
│   ├── composables/          # 组合式函数
│   │   ├── useAuth.ts        # 认证逻辑
│   │   ├── useAgents.ts      # Agent 管理
│   │   ├── useTasks.ts       # 任务管理
│   │   ├── useWebSocket.ts   # WebSocket 连接
│   │   ├── useVNC.ts         # VNC 连接
│   │   └── useNotification.ts # 通知管理
│   ├── pages/                # 页面组件
│   │   ├── auth/
│   │   │   ├── Login.vue
│   │   │   └── Register.vue
│   │   ├── dashboard/
│   │   │   └── Dashboard.vue
│   │   ├── agents/
│   │   │   ├── AgentList.vue
│   │   │   ├── AgentDetail.vue
│   │   │   └── AgentCreate.vue
│   │   ├── tasks/
│   │   │   ├── TaskList.vue
│   │   │   ├── TaskDetail.vue
│   │   │   └── TaskCreate.vue
│   │   ├── settings/
│   │   │   ├── Profile.vue
│   │   │   └── System.vue
│   │   └── NotFound.vue
│   ├── router/               # 路由配置
│   │   └── index.ts
│   ├── stores/               # 状态管理
│   │   ├── auth.ts           # 认证状态
│   │   ├── agents.ts         # Agent 状态
│   │   ├── tasks.ts          # 任务状态
│   │   ├── ui.ts             # UI 状态
│   │   └── index.ts          # Store 入口
│   ├── types/                # 类型定义
│   │   ├── api.ts            # API 类型
│   │   ├── auth.ts           # 认证类型
│   │   ├── agent.ts          # Agent 类型
│   │   ├── task.ts           # 任务类型
│   │   └── common.ts         # 通用类型
│   ├── utils/                # 工具函数
│   │   ├── request.ts        # 请求工具
│   │   ├── storage.ts        # 存储工具
│   │   ├── format.ts         # 格式化工具
│   │   ├── validation.ts     # 验证工具
│   │   └── constants.ts      # 常量定义
│   ├── styles/               # 样式文件
│   │   ├── main.css          # 主样式
│   │   ├── components.css    # 组件样式
│   │   └── utilities.css     # 工具样式
│   ├── App.vue               # 根组件
│   └── main.ts               # 应用入口
├── tests/                    # 测试文件
│   ├── unit/                 # 单元测试
│   │   ├── components/
│   │   ├── composables/
│   │   └── utils/
│   ├── integration/          # 集成测试
│   └── e2e/                  # 端到端测试
├── package.json              # 依赖配置
├── tsconfig.json             # TypeScript 配置
├── vite.config.ts            # Vite 配置
├── tailwind.config.js        # Tailwind 配置
├── .eslintrc.json            # ESLint 配置
├── .prettierrc               # Prettier 配置
└── Dockerfile                # Docker 镜像
```

### 关键文件说明

#### `src/main.ts` - 应用入口
```typescript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// 样式导入
import './styles/main.css'

// 创建应用实例
const app = createApp(App)

// 安装插件
app.use(createPinia())
app.use(router)

// 挂载应用
app.mount('#app')
```

#### `src/router/index.ts` - 路由配置
```typescript
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 路由组件懒加载
const Dashboard = () => import('@/pages/dashboard/Dashboard.vue')
const AgentList = () => import('@/pages/agents/AgentList.vue')
const Login = () => import('@/pages/auth/Login.vue')

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/agents',
    name: 'AgentList',
    component: AgentList,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guest: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
```

---

## 🐍 Backend 目录结构

### 完整目录树

```
backend/
├── app/                        # 应用源代码
│   ├── __init__.py
│   ├── main.py                 # 应用入口
│   ├── config.py               # 配置管理
│   ├── dependencies.py         # 依赖注入
│   ├── exceptions.py           # 异常定义
│   ├── middleware.py           # 中间件
│   │
│   ├── interfaces/             # 接口层
│   │   ├── __init__.py
│   │   ├── api/                # REST API
│   │   │   ├── __init__.py
│   │   │   ├── routes/         # 路由定义
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py     # 认证路由
│   │   │   │   ├── users.py    # 用户路由
│   │   │   │   ├── agents.py   # Agent 路由
│   │   │   │   ├── tasks.py    # 任务路由
│   │   │   │   ├── sandbox.py  # 沙箱路由
│   │   │   │   └── websocket.py # WebSocket 路由
│   │   │   └── dependencies.py # API 依赖
│   │   │
│   │   ├── schemas/            # 数据模式
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # 基础模式
│   │   │   ├── auth.py         # 认证模式
│   │   │   ├── user.py         # 用户模式
│   │   │   ├── agent.py        # Agent 模式
│   │   │   └── task.py         # 任务模式
│   │   │
│   │   └── websocket/          # WebSocket 处理
│   │       ├── __init__.py
│   │       ├── handlers.py     # 消息处理
│   │       ├── manager.py      # 连接管理
│   │       └── events.py       # 事件定义
│   │
│   ├── domain/                 # 领域层
│   │   ├── __init__.py
│   │   ├── models/             # 领域模型
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # 基础模型
│   │   │   ├── user.py         # 用户模型
│   │   │   ├── agent.py        # Agent 模型
│   │   │   ├── task.py         # 任务模型
│   │   │   └── session.py      # 会话模型
│   │   │
│   │   ├── services/           # 领域服务
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py # 认证服务
│   │   │   ├── user_service.py # 用户服务
│   │   │   ├── agent_service.py # Agent 服务
│   │   │   ├── task_service.py # 任务服务
│   │   │   └── sandbox_service.py # 沙箱服务
│   │   │
│   │   ├── repositories/       # 仓储接口
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # 基础仓储
│   │   │   ├── user_repository.py
│   │   │   ├── agent_repository.py
│   │   │   ├── task_repository.py
│   │   │   └── session_repository.py
│   │   │
│   │   └── events/             # 领域事件
│   │       ├── __init__.py
│   │       ├── base.py         # 基础事件
│   │       ├── user_events.py  # 用户事件
│   │       ├── agent_events.py # Agent 事件
│   │       └── task_events.py  # 任务事件
│   │
│   └── infrastructure/         # 基础设施层
│       ├── __init__.py
│       │
│       ├── mongodb/            # MongoDB 集成
│       │   ├── __init__.py
│       │   ├── database.py     # 数据库连接
│       │   ├── repositories/   # 仓储实现
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   ├── user_repository.py
│       │   │   ├── agent_repository.py
│       │   │   ├── task_repository.py
│       │   │   └── session_repository.py
│       │   └── migrations/     # 数据迁移
│       │       ├── __init__.py
│       │       └── init_db.py
│       │
│       ├── redis/              # Redis 集成
│       │   ├── __init__.py
│       │   ├── client.py       # Redis 客户端
│       │   ├── cache.py        # 缓存服务
│       │   ├── pubsub.py       # 发布订阅
│       │   └── session.py      # 会话存储
│       │
│       ├── external/           # 外部服务
│       │   ├── __init__.py
│       │   ├── docker_client.py # Docker 集成
│       │   ├── llm_client.py   # LLM API 集成
│       │   ├── search_client.py # 搜索 API 集成
│       │   ├── email_client.py # 邮件服务
│       │   └── storage_client.py # 文件存储
│       │
│       ├── security/           # 安全服务
│       │   ├── __init__.py
│       │   ├── auth.py         # 认证实现
│       │   ├── permissions.py  # 权限控制
│       │   ├── encryption.py   # 加密服务
│       │   └── rate_limit.py   # 限流服务
│       │
│       └── monitoring/         # 监控服务
│           ├── __init__.py
│           ├── metrics.py      # 指标收集
│           ├── logging.py      # 日志服务
│           └── health.py       # 健康检查
│
├── tests/                      # 测试文件
│   ├── __init__.py
│   ├── conftest.py             # pytest 配置
│   ├── unit/                   # 单元测试
│   │   ├── services/
│   │   ├── repositories/
│   │   └── utils/
│   ├── integration/            # 集成测试
│   │   ├── api/
│   │   ├── database/
│   │   └── external/
│   └── e2e/                    # 端到端测试
│       ├── auth_flow.py
│       ├── agent_lifecycle.py
│       └── task_execution.py
│
├── requirements/               # 依赖文件
│   ├── base.txt                # 基础依赖
│   ├── dev.txt                 # 开发依赖
│   └── prod.txt                # 生产依赖
├── .env.example               # 环境变量模板
├── alembic.ini                # 数据库迁移配置
├── pyproject.toml             # 项目配置
├── Dockerfile                 # Docker 镜像
└── README.md                  # 模块说明
```

### 关键文件说明

#### `app/main.py` - 应用入口
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.infrastructure.mongodb.database import init_database
from app.infrastructure.redis.client import init_redis
from app.interfaces.api.routes import auth, users, agents, tasks
from app.middleware import logging_middleware, error_handler_middleware
from app.infrastructure.monitoring.health import health_check


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    await init_database()
    await init_redis()
    yield
    # 关闭时清理


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI Manus - 通用AI Agent系统",
    lifespan=lifespan
)

# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(logging_middleware)
app.middleware("http")(error_handler_middleware)

# 注册路由
app.include_router(auth.router, prefix="/api/auth")
app.include_router(users.router, prefix="/api/users")
app.include_router(agents.router, prefix="/api/agents")
app.include_router(tasks.router, prefix="/api/tasks")

# 健康检查
app.get("/health")(health_check)
```

#### `app/config.py` - 配置管理
```python
from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""

    # 应用信息
    app_name: str = "AI Manus"
    app_version: str = "1.0.0"
    debug: bool = False

    # 数据库配置
    mongodb_url: str
    redis_url: str

    # 安全配置
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # LLM 配置
    openai_api_key: Optional[str] = None
    openai_base_url: str = "https://api.openai.com/v1"
    model_name: str = "gpt-3.5-turbo"
    max_tokens: int = 2048
    temperature: float = 0.7

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
```

---

## 🐳 Sandbox 目录结构

### 完整目录树

```
sandbox/
├── app/                        # 沙箱应用
│   ├── __init__.py
│   ├── main.py                 # 沙箱服务入口
│   ├── config.py               # 沙箱配置
│   │
│   ├── api/                    # 沙箱 API
│   │   ├── __init__.py
│   │   ├── routes/             # 路由定义
│   │   │   ├── __init__.py
│   │   │   ├── container.py    # 容器管理
│   │   │   ├── files.py        # 文件操作
│   │   │   ├── shell.py        # Shell 命令
│   │   │   ├── browser.py      # 浏览器自动化
│   │   │   └── vnc.py          # VNC 服务
│   │   └── dependencies.py     # API 依赖
│   │
│   ├── services/               # 沙箱服务
│   │   ├── __init__.py
│   │   ├── container_service.py # 容器管理服务
│   │   ├── file_service.py     # 文件操作服务
│   │   ├── shell_service.py    # Shell 执行服务
│   │   ├── browser_service.py  # 浏览器服务
│   │   └── vnc_service.py      # VNC 服务
│   │
│   └── utils/                  # 工具函数
│       ├── __init__.py
│       ├── security.py         # 安全工具
│       ├── validation.py       # 验证工具
│       └── monitoring.py       # 监控工具
│
├── docker/                     # Docker 配置
│   ├── Dockerfile              # 沙箱镜像
│   ├── docker-compose.yml      # 容器编排
│   └── entrypoint.sh           # 启动脚本
│
├── tools/                      # 预装工具
│   ├── install-chrome.sh       # Chrome 安装
│   ├── install-vnc.sh          # VNC 安装
│   └── install-tools.sh        # 开发工具安装
│
├── requirements.txt            # Python 依赖
├── Dockerfile                  # 服务镜像
└── README.md                   # 模块说明
```

### 关键文件说明

#### `app/main.py` - 沙箱服务入口
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import container, files, shell, browser, vnc

# 创建 FastAPI 应用
app = FastAPI(
    title="AI Manus Sandbox",
    description="沙箱环境API服务",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(container.router, prefix="/api/container")
app.include_router(files.router, prefix="/api/files")
app.include_router(shell.router, prefix="/api/shell")
app.include_router(browser.router, prefix="/api/browser")
app.include_router(vnc.router, prefix="/api/vnc")

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "sandbox"}
```

---

## 🎭 MockServer 目录结构

### 完整目录树

```
mockserver/
├── app/                        # 模拟服务应用
│   ├── __init__.py
│   ├── main.py                 # 服务入口
│   ├── config.py               # 服务配置
│   │
│   ├── api/                    # 模拟 API
│   │   ├── __init__.py
│   │   ├── routes/             # 路由定义
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # 认证模拟
│   │   │   ├── agents.py       # Agent 模拟
│   │   │   ├── tasks.py        # 任务模拟
│   │   │   └── llm.py          # LLM 模拟
│   │   └── dependencies.py     # API 依赖
│   │
│   ├── models/                 # 模拟数据模型
│   │   ├── __init__.py
│   │   ├── user.py             # 用户模拟数据
│   │   ├── agent.py            # Agent 模拟数据
│   │   └── task.py             # 任务模拟数据
│   │
│   ├── services/               # 模拟服务
│   │   ├── __init__.py
│   │   ├── data_service.py     # 数据服务
│   │   ├── state_service.py    # 状态管理
│   │   └── response_service.py # 响应生成
│   │
│   └── utils/                  # 工具函数
│       ├── __init__.py
│       ├── generators.py       # 数据生成器
│       └── validators.py       # 验证工具
│
├── data/                       # 模拟数据
│   ├── users.json              # 用户数据
│   ├── agents.json             # Agent 数据
│   └── tasks.json              # 任务数据
│
├── requirements.txt            # Python 依赖
├── Dockerfile                  # 服务镜像
└── README.md                   # 模块说明
```

---

## 📜 Scripts 目录结构

### 完整目录树

```
scripts/
├── build/                      # 构建脚本
│   ├── build-frontend.sh       # 前端构建
│   ├── build-backend.sh        # 后端构建
│   ├── build-sandbox.sh        # 沙箱构建
│   └── build-all.sh            # 全量构建
│
├── deploy/                     # 部署脚本
│   ├── deploy-dev.sh           # 开发环境部署
│   ├── deploy-staging.sh       # 测试环境部署
│   ├── deploy-prod.sh          # 生产环境部署
│   └── rollback.sh             # 回滚脚本
│
├── setup/                      # 环境设置
│   ├── setup-dev.sh            # 开发环境设置
│   ├── install-deps.sh         # 依赖安装
│   ├── init-db.sh              # 数据库初始化
│   └── generate-ssl.sh         # SSL 证书生成
│
├── maintenance/                # 维护脚本
│   ├── backup.sh               # 数据备份
│   ├── cleanup.sh              # 清理脚本
│   ├── update-deps.sh          # 依赖更新
│   └── health-check.sh         # 健康检查
│
├── monitoring/                 # 监控脚本
│   ├── collect-metrics.sh      # 指标收集
│   ├── log-analysis.sh         # 日志分析
│   └── alert.sh                # 告警脚本
│
└── utils/                      # 工具脚本
    ├── wait-for-it.sh          # 服务等待
    ├── generate-env.sh         # 环境变量生成
    └── version-check.sh        # 版本检查
```

---

## 🧪 Tests 目录结构

### 完整目录树

```
tests/
├── __init__.py
├── conftest.py                 # pytest 全局配置
├── fixtures/                   # 测试数据
│   ├── users.json
│   ├── agents.json
│   └── tasks.json
│
├── unit/                       # 单元测试
│   ├── frontend/               # 前端单元测试
│   │   ├── components/
│   │   ├── composables/
│   │   ├── stores/
│   │   └── utils/
│   │
│   └── backend/                # 后端单元测试
│       ├── services/
│       ├── repositories/
│       ├── models/
│       └── utils/
│
├── integration/                # 集成测试
│   ├── api/                    # API 集成测试
│   │   ├── auth_test.py
│   │   ├── users_test.py
│   │   ├── agents_test.py
│   │   └── tasks_test.py
│   │
│   ├── database/               # 数据库集成测试
│   │   ├── mongodb_test.py
│   │   └── redis_test.py
│   │
│   └── external/               # 外部服务集成测试
│       ├── docker_test.py
│       ├── llm_test.py
│       └── search_test.py
│
├── e2e/                        # 端到端测试
│   ├── auth_flow.py            # 认证流程测试
│   ├── agent_lifecycle.py      # Agent 生命周期测试
│   ├── task_execution.py       # 任务执行测试
│   ├── real_time_updates.py    # 实时更新测试
│   └── vnc_integration.py      # VNC 集成测试
│
├── performance/                # 性能测试
│   ├── load_test.py            # 负载测试
│   ├── stress_test.py          # 压力测试
│   └── benchmark.py            # 基准测试
│
└── utils/                      # 测试工具
    ├── helpers.py              # 辅助函数
    ├── assertions.py           # 自定义断言
    └── mocks.py                # 模拟对象
```

---

## 📁 BMad Core 目录结构

### 完整目录树

```
.bmad-core/
├── core-config.yaml            # 核心配置
├── agents/                     # 智能代理配置
│   ├── dev.yaml                # 开发者代理
│   ├── architect.yaml          # 架构师代理
│   └── qa.yaml                 # 测试代理
│
├── tasks/                      # 任务模板
│   ├── create-doc.md           # 文档创建任务
│   ├── execute-checklist.md    # 检查清单执行
│   ├── validate-next-story.md  # 故事验证
│   └── apply-qa-fixes.md       # QA 修复
│
├── templates/                  # 文档模板
│   ├── architecture-tmpl.yaml  # 架构文档模板
│   ├── fullstack-architecture-tmpl.yaml # 全栈架构模板
│   └── prd-tmpl.md             # PRD 文档模板
│
├── checklists/                 # 检查清单
│   ├── architect-checklist.md  # 架构师检查清单
│   ├── dev-checklist.md        # 开发者检查清单
│   └── story-dod-checklist.md  # 故事完成检查清单
│
├── data/                       # 数据文件
│   ├── technical-preferences.md # 技术偏好
│   └── project-config.json     # 项目配置
│
├── utils/                      # 工具函数
│   ├── markdown-helper.py      # Markdown 辅助
│   ├── file-utils.py           # 文件工具
│   └── template-engine.py      # 模板引擎
│
├── cache/                      # 缓存目录
├── logs/                       # 日志目录
└── README.md                   # BMad 框架说明
```

---

## 🔄 文件命名和组织规范

### 命名规范

#### 通用规范
- **文件名**: 使用小写字母和连字符 (`file-name.ext`)
- **目录名**: 使用小写字母和连字符 (`dir-name/`)
- **组件文件**: 使用 PascalCase (`ComponentName.vue`)
- **测试文件**: 添加 `_test` 或 `.test` 后缀

#### 前端文件命名
```
src/
├── components/
│   ├── UserProfile.vue         # PascalCase
│   ├── user-card.vue           # kebab-case (可选)
│   └── TheHeader.vue           # 特殊组件加 The 前缀
├── composables/
│   ├── useAuth.ts              # camelCase with use 前缀
│   ├── useApiRequest.ts
│   └── useLocalStorage.ts
├── stores/
│   ├── auth.ts                 # camelCase
│   ├── userStore.ts
│   └── agentStore.ts
└── types/
    ├── user.ts                 # camelCase
    ├── agent.ts
    └── api-response.ts
```

#### 后端文件命名
```
app/
├── domain/
│   ├── models/
│   │   ├── user.py             # snake_case
│   │   ├── agent_service.py
│   │   └── task_repository.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── agent_service.py
│   └── repositories/
│       ├── base_repository.py
│       ├── user_repository.py
│       └── agent_repository.py
├── interfaces/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── agents.py
│   │   └── schemas/
│   │       ├── user.py
│   │       ├── agent.py
│   │       └── task.py
│   └── websocket/
│       ├── handlers.py
│       └── manager.py
└── infrastructure/
    ├── mongodb/
    │   ├── database.py
    │   └── repositories/
    ├── redis/
    │   ├── client.py
    │   └── cache.py
    └── external/
        ├── docker_client.py
        └── llm_client.py
```

### 目录组织原则

#### 1. 按功能分层
- **interfaces**: 对外接口层 (API, WebSocket)
- **domain**: 业务逻辑层 (Models, Services, Repositories)
- **infrastructure**: 基础设施层 (Database, Cache, External APIs)

#### 2. 按职责分组
- **components**: UI 组件，按类型细分
- **services**: 业务服务，按领域细分
- **utils**: 工具函数，按功能细分

#### 3. 保持扁平
- 避免过深的目录嵌套
- 相关文件放在同一目录
- 使用索引文件简化导入

#### 4. 清晰边界
- 前后端代码分离
- 测试代码就近放置
- 配置文件集中管理

---

## 📈 文件大小和复杂度控制

### 文件大小建议

#### 前端文件
- **组件文件**: < 300 行
- **Composable**: < 200 行
- **Store**: < 300 行
- **类型文件**: < 500 行
- **工具文件**: < 200 行

#### 后端文件
- **路由文件**: < 300 行
- **服务文件**: < 400 行
- **模型文件**: < 300 行
- **仓储文件**: < 300 行
- **工具文件**: < 200 行

### 复杂度控制

#### 1. 单一职责
- 每个文件只负责一个功能
- 避免混合多种职责
- 保持函数简洁

#### 2. 依赖管理
- 明确依赖关系
- 避免循环依赖
- 使用依赖注入

#### 3. 代码复用
- 提取公共逻辑
- 创建基础组件
- 使用继承和组合

---

## 🔍 代码导航和查找

### 常用查找模式

#### 1. 功能查找
```bash
# 查找认证相关代码
find . -name "*auth*" -type f

# 查找 Agent 相关代码
find . -name "*agent*" -type f

# 查找测试文件
find . -name "*test*" -type f
```

#### 2. 类型查找
```bash
# 查找 Python 文件
find . -name "*.py" -type f

# 查找 Vue 组件
find . -name "*.vue" -type f

# 查找 TypeScript 文件
find . -name "*.ts" -type f
```

#### 3. 依赖查找
```bash
# 查找导入关系
grep -r "from.*import" . --include="*.py"

# 查找组件引用
grep -r "import.*from" . --include="*.vue" --include="*.ts"
```

### IDE 配置建议

#### VS Code 工作区配置
```json
{
  "files.exclude": {
    "**/node_modules": true,
    "**/__pycache__": true,
    "**/dist": true,
    "**/.git": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/.git": true
  },
  "files.associations": {
    "*.vue": "vue"
  }
}
```

---

## 📝 文档和注释规范

### 文档组织

#### 1. README 文件
- 每个主要模块都有 README.md
- 说明模块职责和使用方法
- 提供快速开始指南

#### 2. 代码文档
- 公共接口必须有文档字符串
- 复杂逻辑需要行内注释
- 使用 JSDoc/Google Style

#### 3. 架构文档
- 在 `docs/` 目录集中管理
- 使用图表说明架构关系
- 保持文档与代码同步

### 注释规范

#### Python 注释
```python
def create_user(user_data: dict) -> User:
    """创建新用户

    Args:
        user_data: 用户数据字典

    Returns:
        User: 创建的用户对象

    Raises:
        ValueError: 当用户名已存在时
    """
    # 检查用户名唯一性
    existing_user = await self.get_by_username(user_data['username'])
    if existing_user:
        raise ValueError("用户名已存在")

    # 创建用户
    user = User(**user_data)
    return await user.insert()
```

#### TypeScript 注释
```typescript
/**
 * 用户认证 Composable
 *
 * 提供用户登录、注册、登出等功能
 *
 * @example
 * ```typescript
 * const { login, logout, user, isAuthenticated } = useAuth()
 * await login({ username: 'admin', password: 'password' })
 * ```
 */
export function useAuth() {
  // 实现逻辑
}
```

---

## 🚀 最佳实践建议

### 1. 目录结构演进
- 从简单开始，逐步复杂化
- 根据项目规模调整结构
- 保持结构的一致性

### 2. 文件组织策略
- 按功能优先，按类型次要
- 保持相关文件就近
- 使用目录索引文件

### 3. 命名一致性
- 在整个项目中保持命名风格一致
- 使用有意义的名称
- 避免缩写和简写

### 4. 维护性考虑
- 定期重构目录结构
- 清理无用文件
- 更新文档和注释

---

*本文档由 AI 自动生成，涵盖 AI Manus 完整源码结构*
*最后更新时间: 2025-11-05*