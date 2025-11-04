[根目录](../../CLAUDE.md) > **sandbox**

# Sandbox 模块文档

## 变更记录 (Changelog)

**2025-11-04 13:13:53** - 初始化Sandbox模块文档
- 扫描了沙箱环境的Python代码结构
- 分析了Docker容器配置和API服务
- 识别了VNC服务器和工具API的集成方式

## 模块职责

Sandbox模块提供隔离的执行环境，为每个AI Agent会话创建独立的Docker容器。它负责文件操作、Shell命令执行、浏览器自动化、VNC远程桌面等服务，确保Agent在安全可控的环境中执行任务。

## 入口与启动

### 主要入口文件
- **`app/main.py`**: FastAPI应用入口，配置CORS、中间件和路由
- **`requirements.txt`**: Python依赖包列表
- **`Dockerfile`**: 容器构建配置

### 启动配置
- **端口映射**: 8080 (API), 5900 (VNC)
- **环境变量**: LOG_LEVEL, UVI_ARGS等
- **进程管理**: 使用supervisor管理多个服务进程

## 对外接口

### API服务 (`app/api/`)
- **文件系统API**: 文件读写、目录操作
- **Shell API**: 命令执行、会话管理
- **浏览器API**: 页面操作、截图、导航
- **系统API**: 进程管理、资源监控

### VNC服务
- **端口**: 5900标准VNC端口
- **协议**: RFB协议
- **WebSocket转换**: 通过websockify转换为WebSocket
- **认证**: 基于会话的签名URL认证

## 关键依赖与配置

### 核心依赖
```python
fastapi           # Web框架
uvicorn           # ASGI服务器
python-multipart  # 文件上传支持
playwright        # 浏览器自动化
```

### 系统依赖
- **x11vnc**: VNC服务器
- **xvfb**: 虚拟显示框架
- **websockify**: VNC到WebSocket转换
- **supervisor**: 进程管理器
- **Chrome**: 浏览器引擎

### 配置文件
- **`supervisord.conf`**: 进程管理配置
- **`app/core/config.py`**: 应用配置设置
- **`app/core/middleware.py`**: 自定义中间件

## 服务架构

### 进程管理
```
supervisor
├── fastapi-app (API服务)
├── x11vnc (VNC服务)
├── xvfb (虚拟显示)
├── websockify (WebSocket代理)
└── chrome (浏览器进程)
```

### API模块结构
```
app/api/
├── router.py      # 路由聚合
├── files/         # 文件操作API
├── shell/         # Shell命令API
├── browser/       # 浏览器API
└── system/        # 系统监控API
```

## 工具集成

### 文件系统工具
- **文件读写**: 支持文本和二进制文件
- **目录操作**: 创建、删除、列表、权限管理
- **路径安全**: 防止路径遍历攻击
- **存储限制**: 磁盘空间和文件大小限制

### Shell工具
- **命令执行**: 安全的Shell命令执行
- **会话管理**: 维护命令执行上下文
- **输出捕获**: 实时捕获stdout和stderr
- **超时控制**: 防止长时间运行的命令

### 浏览器工具
- **页面导航**: URL跳转和页面加载
- **元素操作**: 点击、输入、选择等交互
- **截图功能**: 页面和元素截图
- **内容提取**: 文本和结构化数据提取

## 安全机制

### 容器隔离
- **文件系统隔离**: 独立的root文件系统
- **网络隔离**: 限制网络访问权限
- **进程隔离**: 容器内进程隔离
- **资源限制**: CPU、内存使用限制

### API安全
- **输入验证**: 严格的参数验证
- **路径安全**: 防止目录遍历
- **命令注入防护**: Shell命令参数化
- **权限控制**: 最小权限原则

### VNC安全
- **会话认证**: 基于签名的URL认证
- **超时控制**: VNC连接自动超时
- **访问日志**: 记录VNC访问行为

## 监控与日志

### 系统监控
- **资源使用**: CPU、内存、磁盘监控
- **进程状态**: 服务进程健康检查
- **网络状态**: 连接状态和流量统计

### 日志系统
- **结构化日志**: JSON格式日志输出
- **日志级别**: 可配置的日志级别
- **日志轮转**: 防止日志文件过大
- **错误追踪**: 异常堆栈记录

## 性能优化

### 资源管理
- **内存优化**: 及时释放不需要的资源
- **连接复用**: 数据库和HTTP连接复用
- **缓存策略**: 常用数据缓存
- **并发控制**: 合理的并发限制

### 响应优化
- **异步处理**: 异步I/O操作
- **流式响应**: 大文件流式传输
- **压缩传输**: Gzip压缩
- **缓存头**: 合理的HTTP缓存策略

## 开发与调试

### 开发模式
```bash
# 开发环境启动
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# 调试模式
LOG_LEVEL=DEBUG uvicorn app.main:app --reload
```

### 调试工具
- **API文档**: `/docs` Swagger UI
- **日志查看**: 容器内日志文件
- **进程监控**: supervisorctl状态检查
- **网络调试**: 端口连通性测试

## 常见问题 (FAQ)

### Q: VNC连接失败怎么办？
A: 检查x11vnc进程状态，确认DISPLAY环境变量，验证websockify配置。

### Q: 文件上传失败怎么处理？
A: 检查磁盘空间，文件权限，multipart配置。

### Q: Shell命令执行超时？
A: 调整命令超时配置，检查命令是否需要交互输入。

### Q: 浏览器启动失败？
A: 确认Chrome安装路径，检查显示环境配置，验证Playwright浏览器安装。

## 相关文件清单

### 应用代码
- `app/main.py` - 应用入口
- `app/api/router.py` - 路由配置
- `app/core/config.py` - 配置管理
- `app/core/middleware.py` - 中间件
- `app/core/exceptions.py` - 异常定义

### API模块
- `app/api/files/` - 文件操作API
- `app/api/shell/` - Shell命令API
- `app/api/browser/` - 浏览器API
- `app/api/system/` - 系统监控API

### 配置文件
- `requirements.txt` - Python依赖
- `Dockerfile` - 容器构建
- `supervisord.conf` - 进程管理配置
- `.dockerignore` - 容器构建忽略文件

### 文档
- `README.md` - 模块说明
- `README_zh.md` - 中文说明

---

*本文档由AI自动生成，最后更新时间: 2025-11-04 13:13:53*