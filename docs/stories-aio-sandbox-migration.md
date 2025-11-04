# AIO Sandbox Migration - 详细用户故事

> **史诗ID**: EPIC-001
> **创建日期**: 2025-11-05
> **产品经理**: Sarah
> **Story Manager**: Claude Assistant
> **项目**: AI Manus Sandbox 技术升级

---

## 📋 故事总览

### 史诗目标
将AI Manus的自建Sandbox模块替换为标准化的AIO Sandbox，实现零风险迁移并获得显著功能增强，同时保持100%的API兼容性和用户体验。

### 故事时间线
- **Story 1**: 1周 - AIO Sandbox技术验证与基础集成
- **Story 2**: 2-3周 - Backend适配层开发与API兼容性保证
- **Story 3**: 1周 - 生产环境切换与旧系统下线

**总预估工期**: 4-5周

---

## 🎯 Story 1: AIO Sandbox技术验证与基础集成

**预估工期**: 1周
**优先级**: P0 - 最高优先级
**故事类型**: 技术验证

### 用户故事描述

**作为** 系统架构师
**我希望** 验证AIO Sandbox可以在AI Manus环境中成功部署并建立基础MCP连接
**以便** 为后续的完整迁移提供技术可行性保证

### 验收标准 (Acceptance Criteria)

#### AC1: AIO Sandbox容器成功部署
- [ ] AIO Sandbox容器可以在开发环境中成功启动
- [ ] 容器健康检查通过，所有服务状态为RUNNING
- [ ] 端口映射正确：API(8080)、VNC(5900)、CDP(9222)
- [ ] 容器资源使用在预期范围内

#### AC2: MCP协议基础连接验证
- [ ] 可以成功连接到AIO Sandbox的MCP Hub
- [ ] MCP工具列表获取成功，包含文件、Shell、浏览器等基础工具
- [ ] 至少3个核心MCP工具调用成功（file_read、shell_exec、browser_navigate）
- [ ] MCP响应格式符合预期标准

#### AC3: VNC功能完整性验证
- [ ] VNC服务正常启动，可通过浏览器访问
- [ ] 远程桌面环境完整，包含Chrome浏览器
- [ ] 基础桌面操作（鼠标、键盘）响应正常
- [ ] 与现有VNC客户端兼容

#### AC4: 与现有Backend集成测试
- [ ] Backend可以成功调用AIO Sandbox API
- [ ] 基础文件操作（读写、列表）功能正常
- [ ] 基础Shell命令执行功能正常
- [ ] 错误处理和异常情况响应正确

### 技术实施步骤

#### 步骤1: 环境准备 (第1-2天)
```bash
# 1. 拉取AIO Sandbox镜像
docker pull ghcr.io/agent-infra/sandbox:latest

# 2. 创建开发测试环境
docker run -d \
  --name aio-sandbox-test \
  -p 8080:8080 \
  -p 5900:5900 \
  -p 9222:9222 \
  ghcr.io/agent-infra/sandbox:latest

# 3. 验证容器状态
docker logs aio-sandbox-test
curl http://localhost:8080/health
```

#### 步骤2: MCP接口验证 (第3-4天)
```python
# 创建MCP连接测试脚本
import httpx
import asyncio

async def test_mcp_connection():
    client = httpx.AsyncClient()

    # 测试MCP工具列表
    response = await client.post("http://localhost:8080/mcp", json={
        "method": "tools/list"
    })
    tools = response.json()

    # 测试基础工具调用
    test_cases = [
        {"method": "tools/call", "params": {"name": "file_read", "arguments": {"path": "/tmp"}}},
        {"method": "tools/call", "params": {"name": "shell_exec", "arguments": {"command": "echo 'test'"}}},
        {"method": "tools/call", "params": {"name": "browser_navigate", "arguments": {"url": "https://example.com"}}}
    ]

    for case in test_cases:
        response = await client.post("http://localhost:8080/mcp", json=case)
        assert response.status_code == 200
        print(f"✅ {case['params']['name']} 测试通过")
```

#### 步骤3: VNC功能测试 (第5天)
```bash
# 1. 测试VNC连接
# 浏览器访问: http://localhost:8080/vnc/index.html?autoconnect=true

# 2. 验证桌面环境
# - 检查Chrome浏览器是否可用
# - 测试基础桌面操作
# - 验证显示分辨率和性能

# 3. 与现有前端VNC客户端兼容性测试
```

#### 步骤4: Backend集成验证 (第6-7天)
```python
# 修改Backend配置，临时指向AIO Sandbox
# 运行现有测试套件，验证基础功能

# 关键测试用例：
# 1. 文件读写操作
# 2. Shell命令执行
# 3. VNC连接建立
# 4. 错误处理机制
```

### 现有功能验证测试

#### 测试套件1: 文件操作完整性
```python
# 执行现有文件操作测试
def test_file_operations_compatibility():
    """验证所有现有文件操作在AIO Sandbox上正常工作"""
    test_cases = [
        "file_read", "file_write", "file_replace",
        "file_search", "file_find", "file_upload", "file_download"
    ]

    for operation in test_cases:
        # 使用现有Backend测试用例
        result = execute_existing_test(operation)
        assert result.success, f"{operation} 功能验证失败"
```

#### 测试套件2: Shell操作完整性
```python
def test_shell_operations_compatibility():
    """验证所有现有Shell操作在AIO Sandbox上正常工作"""
    test_cases = [
        "shell_exec", "shell_view", "shell_wait",
        "shell_write", "shell_kill"
    ]

    for operation in test_cases:
        result = execute_existing_test(operation)
        assert result.success, f"{operation} 功能验证失败"
```

#### 测试套件3: VNC功能完整性
```python
def test_vnc_compatibility():
    """验证VNC功能与现有系统完全兼容"""
    # 1. VNC连接建立
    # 2. 远程桌面显示
    # 3. 浏览器访问
    # 4. 与前端VNC客户端集成
```

### 风险缓解措施

#### 技术风险
- **容器启动失败**: 准备备用镜像版本和本地构建方案
- **MCP接口不兼容**: 开发协议适配层
- **VNC性能问题**: 优化编码和传输参数

#### 时间风险
- **验证时间不足**: 并行执行多个验证任务
- **环境配置复杂**: 准备自动化部署脚本

### 完成定义 (Definition of Done)

- [ ] 所有验收标准全部通过
- [ ] 技术验证报告完成
- [ ] 风险评估和缓解方案文档化
- [ ] 团队知识转移完成
- [ ] 下一个故事的技术依赖全部满足

---

## 🔧 Story 2: Backend适配层开发与API兼容性保证

**预估工期**: 2-3周
**优先级**: P0 - 最高优先级
**故事类型**: 核心开发

### 用户故事描述

**作为** Backend开发工程师
**我希望** 开发完整的AIO Sandbox适配层，保持所有现有API接口完全不变
**以便** 前端和用户可以无感知地切换到新的AIO Sandbox系统

### 验收标准 (Acceptance Criteria)

#### AC1: 适配层架构设计完成
- [ ] 适配层设计符合现有DDD架构模式
- [ ] MCP协议适配接口设计完成
- [ ] 错误处理和重试机制设计完成
- [ ] 性能优化和缓存策略设计完成

#### AC2: 文件操作API完全兼容
- [ ] 所有文件API端点保持现有签名不变
- [ ] `file_read`、`file_write`、`file_replace`等功能完全兼容
- [ ] 文件上传下载功能完全兼容
- [ ] 错误响应格式与现有系统一致

#### AC3: Shell操作API完全兼容
- [ ] 所有Shell API端点保持现有签名不变
- [ ] 会话管理和命令执行功能完全兼容
- [ ] 进程控制和输出捕获功能完全兼容
- [ ] 超时和异常处理机制一致

#### AC4: VNC和浏览器API完全兼容
- [ ] VNC连接建立和URL生成逻辑保持不变
- [ ] 浏览器自动化接口完全兼容
- [ ] CDP协议集成无缝工作
- [ ] WebSocket连接处理正确

#### AC5: 性能和稳定性保证
- [ ] API响应时间不超过现有系统的110%
- [ ] 并发处理能力不低于现有系统
- [ ] 内存和CPU使用在合理范围内
- [ ] 错误率和异常情况处理优于现有系统

### 技术实施步骤

#### 阶段1: 适配层架构设计 (第1-3天)

**1.1 创建适配层基础结构**
```python
# backend/app/infrastructure/external/sandbox/aio_sandbox_adapter.py
from typing import Dict, Any, Optional, BinaryIO
import httpx
import logging
from app.domain.models.tool_result import ToolResult
from app.domain.external.sandbox import Sandbox

class AIOSandboxAdapter(Sandbox):
    """AIO Sandbox MCP适配层"""

    def __init__(self, sandbox_url: str = "http://localhost:8080"):
        self.sandbox_url = sandbox_url
        self.mcp_endpoint = f"{sandbox_url}/mcp"
        self.client = httpx.AsyncClient(timeout=600)
        self.logger = logging.getLogger(__name__)

    async def call_mcp_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """统一MCP工具调用接口"""
        try:
            response = await self.client.post(
                self.mcp_endpoint,
                json={
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": kwargs
                    }
                }
            )
            response.raise_for_status()

            # 转换MCP响应为ToolResult格式
            mcp_result = response.json()
            return self._convert_to_tool_result(mcp_result)

        except Exception as e:
            self.logger.error(f"MCP工具调用失败 {tool_name}: {str(e)}")
            return ToolResult(
                success=False,
                message=f"MCP工具调用失败: {str(e)}",
                data=None
            )

    def _convert_to_tool_result(self, mcp_result: Dict[str, Any]) -> ToolResult:
        """将MCP响应转换为ToolResult格式"""
        return ToolResult(
            success=mcp_result.get("success", True),
            message=mcp_result.get("message", ""),
            data=mcp_result.get("data"),
            error=mcp_result.get("error")
        )
```

**1.2 工具映射设计**
```python
# MCP工具到现有API的映射表
MCP_TOOL_MAPPING = {
    # 文件操作
    "file_read": {
        "mcp_tool": "file_read",
        "params": {"path": "file", "start_line": "start_line", "end_line": "end_line"}
    },
    "file_write": {
        "mcp_tool": "file_write",
        "params": {"path": "file", "content": "content", "append": "append"}
    },
    "file_replace": {
        "mcp_tool": "file_replace",
        "params": {"path": "file", "old_str": "old_str", "new_str": "new_str"}
    },

    # Shell操作
    "shell_exec": {
        "mcp_tool": "shell_exec",
        "params": {"command": "command", "cwd": "exec_dir", "session": "session_id"}
    },
    "shell_view": {
        "mcp_tool": "shell_view",
        "params": {"session": "session_id"}
    },

    # 浏览器操作
    "browser_navigate": {
        "mcp_tool": "browser_navigate",
        "params": {"url": "url"}
    }
}
```

#### 阶段2: 文件操作适配实现 (第4-7天)

**2.1 文件读取适配**
```python
async def file_read(self, file: str, start_line: int = None,
                   end_line: int = None, sudo: bool = False) -> ToolResult:
    """读取文件内容 - 适配AIO Sandbox MCP"""
    params = {"path": file}
    if start_line is not None:
        params["start_line"] = start_line
    if end_line is not None:
        params["end_line"] = end_line
    if sudo:
        params["sudo"] = True

    return await self.call_mcp_tool("file_read", **params)
```

**2.2 文件写入适配**
```python
async def file_write(self, file: str, content: str, append: bool = False,
                    leading_newline: bool = False, trailing_newline: bool = False,
                    sudo: bool = False) -> ToolResult:
    """写入文件内容 - 适配AIO Sandbox MCP"""
    params = {
        "path": file,
        "content": content,
        "append": append
    }
    if leading_newline:
        params["leading_newline"] = True
    if trailing_newline:
        params["trailing_newline"] = True
    if sudo:
        params["sudo"] = True

    return await self.call_mcp_tool("file_write", **params)
```

**2.3 文件上传适配**
```python
async def file_upload(self, file_data: BinaryIO, path: str,
                     filename: str = None) -> ToolResult:
    """文件上传 - 适配AIO Sandbox"""
    # AIO Sandbox可能使用不同的上传机制
    # 需要根据实际MCP工具实现
    files = {"file": (filename or "upload", file_data, "application/octet-stream")}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{self.sandbox_url}/api/v1/file/upload",
            files=files,
            data={"path": path}
        )
        response.raise_for_status()
        return ToolResult(**response.json())
```

#### 阶段3: Shell操作适配实现 (第8-11天)

**3.1 Shell命令执行适配**
```python
async def exec_command(self, session_id: str, exec_dir: str, command: str) -> ToolResult:
    """执行Shell命令 - 适配AIO Sandbox MCP"""
    return await self.call_mcp_tool(
        "shell_exec",
        session=session_id,
        command=command,
        cwd=exec_dir
    )
```

**3.2 Shell会话管理适配**
```python
async def view_shell(self, session_id: str, console: bool = False) -> ToolResult:
    """查看Shell状态 - 适配AIO Sandbox MCP"""
    return await self.call_mcp_tool(
        "shell_view",
        session=session_id,
        console=console
    )

async def wait_for_process(self, session_id: str, seconds: Optional[int] = None) -> ToolResult:
    """等待进程完成 - 适配AIO Sandbox MCP"""
    params = {"session": session_id}
    if seconds is not None:
        params["timeout"] = seconds

    return await self.call_mcp_tool("shell_wait", **params)
```

#### 阶段4: VNC和浏览器适配实现 (第12-15天)

**4.1 VNC适配**
```python
@property
def vnc_url(self) -> str:
    """VNC URL - 保持与现有格式兼容"""
    return f"ws://{self.sandbox_url.split('//')[1].split(':')[0]}:5900"

async def ensure_vnc_ready(self) -> bool:
    """确保VNC服务就绪"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.sandbox_url}/vnc/status")
            return response.status_code == 200
    except Exception:
        return False
```

**4.2 浏览器CDP适配**
```python
@property
def cdp_url(self) -> str:
    """CDP URL - Chrome DevTools Protocol"""
    return f"http://{self.sandbox_url.split('//')[1].split(':')[0]}:9222"

async def get_browser(self) -> Browser:
    """获取浏览器实例 - 适配AIO Sandbox CDP"""
    return PlaywrightBrowser(self.cdp_url)
```

#### 阶段5: 集成测试和性能优化 (第16-21天)

**5.1 完整集成测试**
```python
# 运行完整的回归测试套件
async def run_compatibility_tests():
    """运行完整的兼容性测试"""
    test_suites = [
        test_file_operations_compatibility,
        test_shell_operations_compatibility,
        test_vnc_compatibility,
        test_browser_automation_compatibility
    ]

    for test_suite in test_suites:
        result = await test_suite()
        assert result.success, f"测试套件失败: {test_suite.__name__}"
```

**5.2 性能基准测试**
```python
async def performance_benchmark():
    """性能基准测试"""
    import time

    # 测试API响应时间
    start_time = time.time()
    await file_read("/tmp/test.txt")
    response_time = time.time() - start_time

    # 确保性能不低于现有系统
    assert response_time < 1.0, "API响应时间过长"
```

### 现有功能验证测试

#### 完整回归测试套件
```python
class AIOCompatibilityTestSuite:
    """AIO Sandbox兼容性测试套件"""

    async def test_all_file_operations(self):
        """测试所有文件操作"""
        operations = [
            "file_read", "file_write", "file_replace", "file_search",
            "file_find", "file_exists", "file_delete", "file_list",
            "file_upload", "file_download"
        ]

        for op in operations:
            result = await self.execute_test_case(op)
            assert result.success, f"文件操作 {op} 失败"

    async def test_all_shell_operations(self):
        """测试所有Shell操作"""
        operations = [
            "exec_command", "view_shell", "wait_for_process",
            "write_to_process", "kill_process"
        ]

        for op in operations:
            result = await self.execute_test_case(op)
            assert result.success, f"Shell操作 {op} 失效"

    async def test_vnc_functionality(self):
        """测试VNC功能"""
        # VNC连接测试
        vnc_ready = await self.sandbox.ensure_vnc_ready()
        assert vnc_ready, "VNC服务未就绪"

        # VNC URL格式测试
        vnc_url = self.sandbox.vnc_url
        assert vnc_url.startswith("ws://"), "VNC URL格式不正确"

    async def test_browser_automation(self):
        """测试浏览器自动化"""
        browser = await self.sandbox.get_browser()

        # 基础导航测试
        await browser.navigate("https://example.com")
        title = await browser.get_title()
        assert title, "浏览器导航失败"
```

### 风险缓解措施

#### 技术风险
- **MCP协议不匹配**: 开发协议转换层
- **性能下降**: 实施缓存和优化策略
- **功能缺失**: 开发自定义MCP工具补充

#### 兼容性风险
- **API签名变更**: 严格保持现有接口不变
- **响应格式差异**: 实施格式转换层
- **错误处理不一致**: 统一错误处理机制

### 完成定义 (Definition of Done)

- [ ] 所有现有API端点完全兼容
- [ ] 完整回归测试套件100%通过
- [ ] 性能指标达到或超过现有系统
- [ ] 错误处理和异常情况完善
- [ ] 代码审查和文档更新完成
- [ ] 生产部署准备就绪

---

## 🚀 Story 3: 生产环境切换与旧系统下线

**预估工期**: 1周
**优先级**: P0 - 最高优先级
**故事类型**: 生产部署

### 用户故事描述

**作为** DevOps工程师
**我希望** 实施蓝绿部署策略，无缝切换到AIO Sandbox并安全下线旧系统
**以便** 实现零停机迁移，确保业务连续性和用户体验

### 验收标准 (Acceptance Criteria)

#### AC1: 蓝绿部署环境准备
- [ ] 新环境(AIO Sandbox)完全部署并验证
- [ ] 旧环境(自建Sandbox)保持正常运行
- [ ] 负载均衡器配置完成，支持流量切换
- [ ] 监控和告警系统配置完成

#### AC2: 生产环境无缝切换
- [ ] 流量切换过程零停机
- [ ] 所有API功能正常工作
- [ ] 前端用户完全无感知
- [ ] VNC连接正常建立
- [ ] 实时SSE流正常推送

#### AC3: 系统监控和验证
- [ ] 性能指标监控正常
- [ ] 错误率和异常监控正常
- [ ] 用户行为数据正常
- [ ] 资源使用情况在预期范围

#### AC4: 旧系统安全下线
- [ ] 新系统稳定运行24小时以上
- [ ] 所有功能验证通过
- [ ] 数据备份和清理完成
- [ ] 旧容器和镜像安全移除

### 技术实施步骤

#### 阶段1: 部署准备 (第1-2天)

**1.1 生产环境配置**
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # 新AIO Sandbox环境
  aio-sandbox:
    image: ghcr.io/agent-infra/sandbox:latest
    container_name: aio-sandbox-prod
    ports:
      - "8080:8080"
      - "5900:5900"
      - "9222:9222"
    environment:
      - SERVICE_TIMEOUT_MINUTES=1440
      - LOG_LEVEL=INFO
    networks:
      - ai-manus-network
    restart: unless-stopped

  # 保留旧Sandbox环境（备用）
  legacy-sandbox:
    image: ai-manus/sandbox:latest
    container_name: legacy-sandbox-backup
    ports:
      - "8081:8080"
      - "5901:5900"
    networks:
      - ai-manus-network
    restart: unless-stopped
    profiles:
      - backup

networks:
  ai-manus-network:
    external: true
```

**1.2 负载均衡器配置**
```nginx
# nginx.conf
upstream sandbox_backend {
    server 127.0.0.1:8080;  # AIO Sandbox (新)
    # server 127.0.0.1:8081; # Legacy Sandbox (旧，备用)
}

server {
    listen 80;
    server_name sandbox.ai-manus.com;

    location / {
        proxy_pass http://sandbox_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # VNC WebSocket代理
    location /vnc/ {
        proxy_pass http://sandbox_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

#### 阶段2: 切换实施 (第3-4天)

**2.1 流量切换脚本**
```bash
#!/bin/bash
# switch_to_aio_sandbox.sh

set -e

echo "开始切换到AIO Sandbox..."

# 1. 验证新系统状态
echo "验证AIO Sandbox状态..."
curl -f http://localhost:8080/health || {
    echo "❌ AIO Sandbox健康检查失败"
    exit 1
}

# 2. 备份当前配置
echo "备份当前配置..."
cp nginx.conf nginx.conf.backup.$(date +%Y%m%d_%H%M%S)

# 3. 更新负载均衡器配置
echo "更新负载均衡器配置..."
sed -i 's/# server 127.0.0.1:8081/server 127.0.0.1:8081/' nginx.conf
sed -i 's/server 127.0.0.1:8080/# server 127.0.0.1:8080/' nginx.conf

# 4. 重新加载Nginx配置
echo "重新加载Nginx配置..."
nginx -t && nginx -s reload

# 5. 验证切换结果
echo "验证切换结果..."
sleep 5
curl -f http://localhost/vnc/ || {
    echo "❌ 切换后验证失败，回滚..."
    cp nginx.conf.backup.$(date +%Y%m%d_%H%M%S) nginx.conf
    nginx -s reload
    exit 1
}

echo "✅ 成功切换到AIO Sandbox"
```

**2.2 健康检查脚本**
```bash
#!/bin/bash
# health_check.sh

set -e

API_ENDPOINT="http://localhost/api/v1/supervisor/status"
VNC_ENDPOINT="http://localhost/vnc/index.html"

echo "执行系统健康检查..."

# API健康检查
echo "检查API状态..."
api_response=$(curl -s -w "%{http_code}" "$API_ENDPOINT")
http_code="${api_response: -3}"
response_body="${api_response%???}"

if [ "$http_code" != "200" ]; then
    echo "❌ API健康检查失败 (HTTP $http_code)"
    exit 1
fi

echo "✅ API健康检查通过"

# VNC健康检查
echo "检查VNC状态..."
vnc_response=$(curl -s -w "%{http_code}" "$VNC_ENDPOINT")
vnc_http_code="${vnc_response: -3}"

if [ "$vnc_http_code" != "200" ]; then
    echo "❌ VNC健康检查失败 (HTTP $vnc_http_code)"
    exit 1
fi

echo "✅ VNC健康检查通过"
echo "✅ 系统整体健康状态良好"
```

#### 阶段3: 监控验证 (第5-6天)

**3.1 实时监控脚本**
```python
# monitor_migration.py
import asyncio
import httpx
import time
from datetime import datetime

class MigrationMonitor:
    def __init__(self):
        self.api_endpoint = "http://localhost/api/v1/supervisor/status"
        self.metrics = []

    async def monitor_system_health(self, duration_hours=24):
        """监控系统健康状态"""
        start_time = time.time()
        end_time = start_time + (duration_hours * 3600)

        while time.time() < end_time:
            try:
                # API响应时间监控
                response_time = await self.measure_api_response_time()

                # 错误率监控
                error_rate = await self.measure_error_rate()

                # 资源使用监控
                resource_usage = await self.get_resource_usage()

                # 记录指标
                self.metrics.append({
                    "timestamp": datetime.now(),
                    "response_time": response_time,
                    "error_rate": error_rate,
                    "cpu_usage": resource_usage["cpu"],
                    "memory_usage": resource_usage["memory"]
                })

                print(f"[{datetime.now()}] 响应时间: {response_time:.3f}s, "
                      f"错误率: {error_rate:.2%}, CPU: {resource_usage['cpu']:.1%}, "
                      f"内存: {resource_usage['memory']:.1%}")

                await asyncio.sleep(300)  # 5分钟检查一次

            except Exception as e:
                print(f"❌ 监控异常: {e}")
                await asyncio.sleep(60)

    async def measure_api_response_time(self):
        """测量API响应时间"""
        start_time = time.time()
        async with httpx.AsyncClient() as client:
            await client.get(self.api_endpoint)
        return time.time() - start_time

    async def measure_error_rate(self):
        """测量错误率"""
        # 实现错误率统计逻辑
        pass

    async def get_resource_usage(self):
        """获取资源使用情况"""
        # 实现资源监控逻辑
        pass

# 启动监控
monitor = MigrationMonitor()
asyncio.run(monitor.monitor_system_health(24))
```

**3.2 自动化告警**
```yaml
# prometheus_rules.yml
groups:
  - name: sandbox_migration_rules
    rules:
      - alert: HighResponseTime
        expr: sandbox_api_response_time > 1.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Sandbox API响应时间过高"

      - alert: HighErrorRate
        expr: sandbox_error_rate > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Sandbox错误率过高"

      - alert: VNCConnectionFailure
        expr: sandbox_vnc_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "VNC服务不可用"
```

#### 阶段4: 旧系统下线 (第7天)

**4.1 安全下线脚本**
```bash
#!/bin/bash
# decommission_legacy_sandbox.sh

set -e

echo "开始下线旧Sandbox系统..."

# 1. 确认新系统稳定运行
echo "确认新系统状态..."
if ! ./health_check.sh; then
    echo "❌ 新系统状态不稳定，终止下线操作"
    exit 1
fi

# 2. 停止旧Sandbox容器
echo "停止旧Sandbox容器..."
docker stop legacy-sandbox-backup || true
docker rm legacy-sandbox-backup || true

# 3. 清理相关镜像（可选）
read -p "是否清理旧Sandbox镜像? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "清理旧Sandbox镜像..."
    docker rmi ai-manus/sandbox:latest || true
fi

# 4. 更新配置文件
echo "更新配置文件..."
sed -i '/legacy-sandbox/,/^$/d' docker-compose.prod.yml

# 5. 清理备份配置
echo "清理备份配置..."
find . -name "nginx.conf.backup.*" -mtime +7 -delete

echo "✅ 旧Sandbox系统成功下线"
```

**4.2 数据备份和清理**
```bash
#!/bin/bash
# backup_and_cleanup.sh

BACKUP_DIR="/backup/sandbox_migration/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "备份重要数据..."

# 1. 备份配置文件
cp -r docker-compose* "$BACKUP_DIR/"
cp -r nginx* "$BACKUP_DIR/"

# 2. 备份日志文件
docker logs aio-sandbox-prod > "$BACKUP_DIR/aio_sandbox.log" 2>&1

# 3. 备份测试结果
cp -r test_results/ "$BACKUP_DIR/" 2>/dev/null || true

echo "数据备份完成: $BACKUP_DIR"

# 4. 清理临时文件
find /tmp -name "sandbox_*" -mtime +1 -delete 2>/dev/null || true

echo "✅ 数据备份和清理完成"
```

### 现有功能验证测试

#### 生产环境验证清单
```python
class ProductionValidationSuite:
    """生产环境验证测试套件"""

    async def test_all_critical_paths(self):
        """测试所有关键路径"""
        test_cases = [
            ("用户会话创建", self.test_session_creation),
            ("文件上传下载", self.test_file_operations),
            ("Shell命令执行", self.test_shell_operations),
            ("VNC连接建立", self.test_vnc_connection),
            ("浏览器自动化", self.test_browser_automation),
            ("实时事件流", self.test_sse_stream),
            ("WebSocket连接", self.test_websocket_connection)
        ]

        for test_name, test_func in test_cases:
            try:
                await test_func()
                print(f"✅ {test_name} - 通过")
            except Exception as e:
                print(f"❌ {test_name} - 失败: {e}")
                raise

    async def test_user_experience(self):
        """测试用户体验"""
        # 1. 页面加载时间
        load_time = await self.measure_page_load_time()
        assert load_time < 3.0, "页面加载时间过长"

        # 2. API响应时间
        api_time = await self.measure_api_response_time()
        assert api_time < 1.0, "API响应时间过长"

        # 3. VNC连接延迟
        vnc_latency = await self.measure_vnc_latency()
        assert vnc_latency < 200, "VNC连接延迟过高"
```

#### 回滚测试
```bash
#!/bin/bash
# rollback_test.sh

echo "执行回滚测试..."

# 1. 模拟切换回旧系统
echo "切换回旧Sandbox..."
sed -i 's/server 127.0.0.1:8080/# server 127.0.0.1:8080/' nginx.conf
sed -i 's/# server 127.0.0.1:8081/server 127.0.0.1:8081/' nginx.conf
nginx -s reload

# 2. 验证旧系统功能
sleep 5
if ./health_check.sh; then
    echo "✅ 回滚测试成功"
else
    echo "❌ 回滚测试失败"
    exit 1
fi

# 3. 恢复到新系统
echo "恢复到AIO Sandbox..."
sed -i 's/# server 127.0.0.1:8080/server 127.0.0.1:8080/' nginx.conf
sed -i 's/server 127.0.0.1:8081/# server 127.0.0.1:8081/' nginx.conf
nginx -s reload

echo "✅ 回滚测试完成，系统已恢复到AIO Sandbox"
```

### 风险缓解措施

#### 运维风险
- **切换失败**: 准备5分钟快速回滚方案
- **性能下降**: 实时监控和自动告警
- **数据丢失**: 完整备份和恢复方案

#### 业务风险
- **用户感知**: 零停机切换策略
- **功能异常**: 并行运行验证期
- **服务中断**: 多层健康检查机制

### 完成定义 (Definition of Done)

- [ ] 生产环境成功切换到AIO Sandbox
- [ ] 所有功能验证测试100%通过
- [ ] 系统稳定运行24小时以上
- [ ] 性能指标达到预期标准
- [ ] 旧系统安全下线
- [ ] 运维文档更新完成
- [ ] 团队知识转移完成

---

## 📊 整体验收标准

### 史诗完成标准

#### 功能完整性
- [ ] 所有现有功能100%保持
- [ ] 新增功能正常工作
- [ ] API接口完全兼容
- [ ] 前端零感知切换

#### 性能指标
- [ ] API响应时间 ≤ 现有系统110%
- [ ] 并发处理能力 ≥ 现有系统
- [ ] 错误率 ≤ 现有系统
- [ ] 资源使用效率提升

#### 质量保证
- [ ] 完整回归测试套件通过
- [ ] 生产环境稳定运行验证
- [ ] 监控和告警系统完善
- [ ] 回滚方案验证可行

#### 文档和知识
- [ ] 技术文档更新完成
- [ ] 运维手册更新完成
- [ ] 团队培训完成
- [ ] 最佳实践文档化

---

## 🔗 相关文档和资源

### 技术文档
- **史诗文件**: `docs/epic-aio-sandbox-migration.md`
- **架构研究报告**: `docs/ai-manus-sandbox-to-aio-sandbox-migration-report.md`
- **AIO Sandbox官方文档**: https://github.com/agent-infra/sandbox
- **MCP协议规范**: https://modelcontextprotocol.io/

### 测试资源
- **现有测试套件**: `backend/tests/`
- **性能基准数据**: 基于现有系统测量
- **监控配置**: Prometheus + Grafana配置

### 部署资源
- **Docker镜像**: ghcr.io/agent-infra/sandbox:latest
- **容器编排**: docker-compose配置
- **负载均衡**: Nginx配置
- **监控告警**: Prometheus规则配置

---

## 📈 成功指标和业务价值

### 技术收益
- **标准化程度**: 采用MCP和CDP行业标准协议
- **维护成本**: 从自维护转向社区维护，预估降低60%
- **开发效率**: 内置开发环境，预估提升40%
- **系统稳定性**: 社区验证的稳定性和安全性

### 业务收益
- **功能增强**: 获得Jupyter、VSCode等开发能力
- **生态集成**: 接入丰富的AI Agent生态系统
- **扩展性**: 基于标准的无限扩展能力
- **竞争优势**: 技术架构现代化和标准化

### 风险控制
- **零停机**: 蓝绿部署确保业务连续性
- **功能保持**: 100%现有功能兼容
- **快速回滚**: 5分钟内回滚能力
- **渐进验证**: 分阶段降低实施风险

---

*用户故事制定完成，准备交付开发团队执行*

*最后更新时间: 2025-11-05*