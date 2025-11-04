[根目录](../../CLAUDE.md) > **mockserver**

# MockServer 模块文档

## 变更记录 (Changelog)

**2025-11-04 13:13:53** - 初始化MockServer模块文档
- 扫描了模拟服务器的Python代码
- 分析了LLM响应模拟和配置管理
- 识别了开发环境辅助功能

## 模块职责

MockServer模块为开发环境提供模拟服务，主要用于模拟LLM API响应，支持开发和测试阶段的离线工作。它提供可配置的延迟、多种响应格式和灵活的模拟数据管理。

## 入口与启动

### 主要入口文件
- **`main.py`**: FastAPI应用入口，配置路由和中间件
- **`requirements.txt`**: Python依赖包列表
- **`Dockerfile`**: 容器构建配置

### 启动配置
- **默认端口**: 8090
- **环境变量**:
  - `MOCK_DATA_FILE`: 模拟数据文件路径
  - `MOCK_DELAY`: 响应延迟时间（秒）

## 对外接口

### 模拟API端点
- **`/v1/chat/completions`**: 模拟OpenAI聊天完成API
- **`/v1/models`**: 模拟模型列表API
- **`/health`**: 健康检查端点
- **`/config`**: 配置查看端点

### 响应格式
完全兼容OpenAI API格式，支持：
- Chat completions响应
- Function calling格式
- Streaming响应
- 错误响应格式

## 关键依赖与配置

### 核心依赖
```python
fastapi       # Web框架
uvicorn       # ASGI服务器
pydantic      # 数据验证
pyyaml        # YAML配置文件解析
```

### 配置管理
- **YAML配置**: 支持复杂的模拟场景配置
- **环境变量覆盖**: 可通过环境变量调整配置
- **热重载**: 开发模式下配置文件热重载

## 模拟数据管理

### 数据文件格式
```yaml
# default.yaml示例
responses:
  - pattern: ".*"
    response:
      choices:
        - message:
            content: "这是一个模拟的AI响应"
      usage:
        prompt_tokens: 10
        completion_tokens: 5
delay: 1.0
```

### 响应匹配策略
- **正则表达式**: 支持请求内容模式匹配
- **优先级排序**: 按配置顺序匹配
- **默认响应**: 未匹配时的默认行为

## 功能特性

### 延迟模拟
- **固定延迟**: 统一的响应延迟
- **随机延迟**: 范围内的随机延迟
- **智能延迟**: 基于内容长度的动态延迟

### 多种模拟模式
- **静态响应**: 预定义的固定响应
- **模板响应**: 基于请求生成响应
- **脚本响应**: Python脚本生成复杂响应

### 开发辅助
- **请求日志**: 记录所有API请求
- **响应日志**: 记录生成的响应
- **错误模拟**: 模拟各种错误场景

## 开发与调试

### 开发模式启动
```bash
# 开发环境
python main.py

# Docker环境
docker build -t mockserver .
docker run -p 8090:8090 mockserver
```

### 调试功能
- **详细日志**: 请求响应详细日志
- **配置检查**: 配置文件验证
- **健康检查**: 服务状态监控

## 集成方式

### Backend集成
在backend的配置中设置：
```env
API_BASE=http://mockserver:8090/v1
API_KEY=mock-key
```

### 测试场景
- **单元测试**: 模拟API响应
- **集成测试**: 端到端测试模拟
- **性能测试**: 响应时间测试

## 扩展能力

### 自定义模拟器
- **插件系统**: 支持自定义模拟器
- **脚本扩展**: Python脚本扩展
- **外部集成**: 外部数据源集成

### 高级功能
- **状态管理**: 有状态的模拟场景
- **并发控制**: 多用户场景模拟
- **性能监控**: 响应时间统计

## 常见问题 (FAQ)

### Q: 如何添加新的模拟场景？
A: 在YAML配置文件中添加新的响应模式，支持正则表达式匹配。

### Q: 如何模拟不同的错误？
A: 配置错误响应格式，设置相应的HTTP状态码和错误消息。

### Q: 如何调整响应延迟？
A: 通过MOCK_DELAY环境变量或配置文件中的delay设置。

### Q: 如何查看请求日志？
A: 检查控制台输出或配置日志文件路径。

## 相关文件清单

### 核心文件
- `main.py` - 应用入口和路由
- `requirements.txt` - Python依赖
- `Dockerfile` - 容器构建配置

### 配置文件
- `default.yaml` - 默认模拟数据
- `test.yaml` - 测试场景配置
- `error.yaml` - 错误场景配置

### 文档
- `README.md` - 使用说明
- `examples/` - 配置示例目录

---

*本文档由AI自动生成，最后更新时间: 2025-11-04 13:13:53*