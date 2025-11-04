[根目录](../../CLAUDE.md) > **backend**

# Backend 模块文档

## 变更记录 (Changelog)

**2025-11-04 13:13:53** - 初始化Backend模块文档
- 扫描了120个Python文件，采用DDD分层架构
- 识别出4层架构：Application、Domain、Infrastructure、Interfaces
- 分析了Agent服务、工具集成和API路由设计

## 模块职责

Backend模块负责核心业务逻辑、AI Agent管理、工具集成和API服务。采用Domain-Driven Design (DDD)架构模式，提供RESTful API和实时事件流，支持用户认证、会话管理、文件操作和沙箱环境管理。

## 入口与启动

### 主要入口文件
- **`app/main.py`**: FastAPI应用入口，配置中间件、路由和生命周期
- **`requirements.txt`**: Python依赖包列表

### 启动流程
1. 初始化日志系统
2. 加载配置设置
3. 连接MongoDB和Redis
4. 初始化Beanie ODM
5. 注册异常处理器和路由
6. 启动FastAPI应用

## 对外接口

### API路由 (`app/interfaces/api/`)
- **`routes.py`**: 主路由聚合器
- **`session_routes.py`**: 会话管理API（CRUD、聊天、文件操作、VNC）
- **`auth_routes.py`**: 用户认证API（登录、注册、令牌管理）
- **`file_routes.py`**: 文件上传下载API

### WebSocket支持
- **VNC WebSocket**: `/sessions/{session_id}/vnc` - 实时VNC数据传输
- **SSE流**: `/sessions/{session_id}/chat` - Agent执行事件流
- **会话列表流**: `/sessions` - 实时会话列表更新

### API文档
- **Swagger UI**: `/docs` - 交互式API文档
- **ReDoc**: `/redoc` - API文档替代界面

## 关键依赖与配置

### 核心依赖
```python
fastapi          # Web框架
uvicorn          # ASGI服务器
openai           # LLM API客户端
pydantic         # 数据验证
beanie           # MongoDB ODM
motor            # MongoDB异步驱动
redis            # Redis客户端
playwright       # 浏览器自动化
docker           # Docker SDK
sse-starlette    # SSE支持
```

### 配置管理 (`app/core/config.py`)
- **LLM配置**: API密钥、模型名称、温度参数
- **数据库配置**: MongoDB和Redis连接
- **沙箱配置**: Docker镜像、网络、TTL设置
- **认证配置**: JWT密钥、加密算法、过期时间
- **搜索引擎配置**: Bing/Google/Baidu API设置

## 架构分层

### 1. Application Layer (`app/application/`)
应用服务层，编排领域服务，处理用例逻辑。
- **`services/agent_service.py`**: Agent核心业务逻辑
- **`services/auth_service.py`**: 认证业务逻辑
- **`services/file_service.py`**: 文件管理业务逻辑
- **`services/token_service.py`**: JWT令牌管理
- **`services/email_service.py`**: 邮件服务

### 2. Domain Layer (`app/domain/`)
领域层，包含核心业务逻辑和领域模型。
- **`models/`**: 领域模型（Agent、Session、User、Plan等）
- **`services/`**: 领域服务（Agent执行、工具调用、流程控制）
- **`repositories/`**: 仓储接口定义
- **`external/`**: 外部服务接口抽象

### 3. Infrastructure Layer (`app/infrastructure/`)
基础设施层，实现技术细节和外部集成。
- **`storage/`**: 数据存储实现（MongoDB、Redis）
- **`repositories/`**: 仓储具体实现
- **`external/`**: 外部服务实现（LLM、浏览器、搜索等）
- **`logging.py`**: 日志基础设施

### 4. Interfaces Layer (`app/interfaces/`)
接口层，处理HTTP请求响应和数据转换。
- **`api/`**: REST API路由
- **`schemas/`**: 请求响应数据模型
- **`dependencies.py`**: 依赖注入配置
- **`errors/`**: 异常处理器

## 数据模型

### 核心领域模型 (`app/domain/models/`)
- **`agent.py`**: Agent实体，管理AI代理状态和配置
- **`session.py`**: 会话实体，跟踪用户对话和执行状态
- **`user.py`**: 用户实体，认证和权限管理
- **`plan.py`**: 执行计划，任务分解和步骤管理
- **`message.py`**: 消息实体，对话内容记录
- **`file.py`**: 文件信息实体，元数据管理

### 文档模型 (`app/infrastructure/models/documents.py`)
- **AgentDocument**: MongoDB中的Agent文档
- **SessionDocument**: MongoDB中的Session文档
- **UserDocument**: MongoDB中的User文档

## 领域服务

### Agent服务 (`app/domain/services/`)
- **`agents/base.py`**: Agent基类，定义通用行为
- **`agents/planner.py`**: 规划Agent，任务分解和计划生成
- **`agents/execution.py`**: 执行Agent，具体任务执行
- **`flows/plan_act.py`**: Plan-Act流程控制
- **`tools/`**: 工具系统（搜索、浏览器、Shell、文件等）

### 工具集成
- **`tools/search.py`**: 网络搜索工具
- **`tools/browser.py`**: 浏览器自动化工具
- **`tools/shell.py`**: Shell命令执行工具
- **`tools/file.py`**: 文件操作工具
- **`tools/mcp.py`**: MCP协议工具

## 外部集成

### LLM集成 (`app/infrastructure/external/llm/`)
- **`openai_llm.py`**: OpenAI兼容API客户端
- 支持Function Calling和JSON模式输出

### 浏览器自动化 (`app/infrastructure/external/browser/`)
- **`playwright_browser.py`**: Playwright浏览器控制
- 支持Chrome Headless模式和截图

### 搜索引擎 (`app/infrastructure/external/search/`)
- **`bing_search.py`**: Bing搜索API
- **`google_search.py`**: Google搜索API
- **`baidu_search.py`**: 百度搜索API

### 沙箱管理 (`app/infrastructure/external/sandbox/`)
- **`docker_sandbox.py`**: Docker容器管理
- 容器生命周期管理和资源隔离

### 缓存和队列
- **`cache/redis_cache.py`**: Redis缓存实现
- **`message_queue/redis_stream_queue.py`**: Redis流队列
- **`task/redis_task.py`**: 异步任务管理

## 测试与质量

### 测试结构
- **`tests/`**: 测试目录
- **`tests/requirements.txt`**: 测试依赖
- 使用pytest作为测试框架

### 代码质量
- **类型注解**: 全面的Python类型提示
- **异步编程**: 基于asyncio的异步架构
- **错误处理**: 统一异常处理机制
- **日志记录**: 结构化日志系统

## 安全机制

### 认证授权
- **JWT认证**: 无状态令牌认证
- **密码加密**: bcrypt哈希加密
- **权限控制**: 基于用户角色的访问控制

### 数据安全
- **输入验证**: Pydantic模型验证
- **SQL注入防护**: 使用ORM和参数化查询
- **XSS防护**: 输出转义和CSP配置

### 沙箱安全
- **容器隔离**: Docker容器资源隔离
- **网络限制**: 容器网络访问控制
- **文件系统隔离**: 独立的文件系统命名空间

## 性能优化

### 数据库优化
- **索引策略**: MongoDB查询优化
- **连接池**: 数据库连接复用
- **缓存策略**: Redis缓存热点数据

### 异步处理
- **异步I/O**: 全异步架构设计
- **任务队列**: Redis异步任务处理
- **流式响应**: SSE实时数据推送

## 常见问题 (FAQ)

### Q: 如何添加新的工具？
A: 在 `app/domain/services/tools/` 创建工具类，实现BaseTool接口，然后在Agent中注册。

### Q: 如何扩展API端点？
A: 在 `app/interfaces/api/` 添加路由文件，定义schemas，并在主路由中注册。

### Q: 如何配置新的LLM提供商？
A: 在 `app/infrastructure/external/llm/` 实现新的LLM客户端，更新配置选项。

### Q: 沙箱容器如何管理？
A: 通过Docker SDK动态创建和销毁容器，使用Redis跟踪容器状态。

## 相关文件清单

### 配置文件
- `requirements.txt` - Python依赖
- `Dockerfile` - 容器构建配置
- `app/core/config.py` - 配置管理

### 核心服务
- `app/application/services/agent_service.py` - Agent核心服务
- `app/domain/services/agents/planner.py` - 规划Agent
- `app/domain/services/agents/execution.py` - 执行Agent

### API层
- `app/interfaces/api/session_routes.py` - 会话API
- `app/interfaces/api/auth_routes.py` - 认证API
- `app/interfaces/schemas/` - 数据模型定义

### 基础设施
- `app/infrastructure/storage/mongodb.py` - MongoDB集成
- `app/infrastructure/storage/redis.py` - Redis集成
- `app/infrastructure/external/sandbox/docker_sandbox.py` - 沙箱管理

---

*本文档由AI自动生成，最后更新时间: 2025-11-04 13:13:53*