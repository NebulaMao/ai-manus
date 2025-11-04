[根目录](../../CLAUDE.md) > **frontend**

# Frontend 模块文档

## 变更记录 (Changelog)

**2025-11-04 13:13:53** - 初始化Frontend模块文档
- 扫描了43个TypeScript文件和62个Vue组件
- 识别出12个composables和89个UI组件
- 分析了API集成和实时通信机制

## 模块职责

Frontend模块负责用户界面展示、实时通信、工具可视化和用户交互。它采用Vue 3 + TypeScript + Vite技术栈，提供响应式的Web界面，支持多语言、主题切换和实时数据展示。

## 入口与启动

### 主要入口文件
- **`src/main.ts`**: 应用程序入口，配置路由、i18n和全局中间件
- **`src/App.vue`**: 根组件，定义应用布局结构
- **`vite.config.ts`**: Vite构建配置，包含Monaco Editor插件

### 路由配置
```typescript
// 主要路由结构
/ -> HomePage (需要认证)
/chat/:sessionId -> ChatPage (需要认证)
/login -> LoginPage
/share/:sessionId -> SharePage (公开访问)
```

## 对外接口

### API集成 (`src/api/`)
- **`client.ts`**: HTTP客户端基础配置，API响应处理
- **`auth.ts`**: 用户认证相关API（登录、注册、令牌刷新）
- **`agent.ts`**: Agent会话管理API（创建、聊天、文件操作）
- **`file.ts`**: 文件上传下载API

### 实时通信
- **SSE连接**: 用于接收Agent执行事件的实时流
- **WebSocket**: 用于VNC远程桌面的实时数据传输
- **事件总线**: 组件间通信机制

## 关键依赖与配置

### 核心依赖
```json
{
  "vue": "^3.3.4",
  "vue-router": "^4.5.1",
  "typescript": "^5.1.3",
  "vite": "^4.3.9",
  "@microsoft/fetch-event-source": "^2.0.1",
  "@novnc/novnc": "^1.5.0",
  "monaco-editor": "^0.52.2"
}
```

### UI框架
- **Reka UI**: 无样式组件库
- **Tailwind CSS**: 样式框架
- **Framer Motion**: 动画库
- **Lucide Vue**: 图标库

### 开发工具
- **Vue TSC**: TypeScript类型检查
- **ESLint**: 代码规范检查
- **PostCSS**: CSS处理

## 数据模型

### 类型定义 (`src/types/`)
- **`event.ts`**: SSE事件类型定义
- **`message.ts`**: 消息和聊天相关类型
- **`response.ts`**: API响应类型
- **`panel.ts`**: 面板和布局类型
- **`router.d.ts`**: 路由类型扩展

### 状态管理
使用Vue 3 Composition API进行状态管理，主要通过composables实现：
- **`useAuth.ts`**: 用户认证状态
- **useI18n**: 国际化配置
- **useDialog**: 对话框状态管理
- **useLeftPanel/useRightPanel**: 面板状态

## 测试与质量

### 当前状态
- ⚠️ 单元测试框架待配置
- ⚠️ 组件测试覆盖率待提升
- ⚠️ E2E测试待实现
- ✅ TypeScript严格模式已启用

### 代码质量工具
- **ESLint**: 代码规范检查
- **Prettier**: 代码格式化
- **TypeScript**: 静态类型检查
- **Vue TSC**: Vue组件类型检查

## 组件架构

### 页面组件 (`src/pages/`)
- **`MainLayout.vue`**: 主布局容器
- **`HomePage.vue`**: 会话列表页面
- **`ChatPage.vue`**: 聊天界面
- **`LoginPage.vue`**: 登录页面
- **`SharePage.vue`**: 共享会话页面

### 核心组件 (`src/components/`)
- **`ChatBox.vue`**: 聊天消息容器
- **`ToolPanel.vue`**: 工具面板容器
- **`FilePanel.vue`**: 文件管理面板
- **`VNCViewer.vue`**: VNC远程桌面查看器
- **`PlanPanel.vue`**: 执行计划展示

### 工具视图 (`src/components/toolViews/`)
- **`ShellToolView.vue`**: Shell工具界面
- **`BrowserToolView.vue`**: 浏览器工具界面
- **`FileToolView.vue`**: 文件工具界面
- **`SearchToolView.vue`**: 搜索工具界面
- **`McpToolView.vue`**: MCP工具界面

### UI组件 (`src/components/ui/`)
- **对话框组件**: 基于Reka UI的对话框系统
- **选择器组件**: 自定义下拉选择器
- **加载指示器**: 各种加载状态组件
- **Toast通知**: 消息提示组件

## 国际化支持

### 语言配置 (`src/locales/`)
- **`zh.ts`**: 中文语言包
- **`en.ts`**: 英文语言包
- **`index.ts`**: i18n配置和初始化

### 使用方式
```typescript
// 在组件中使用
const { t } = useI18n()
const message = t('common.save')
```

## 样式系统

### 主题配置
- **`assets/theme.css`**: 主题变量定义
- **`assets/global.css`**: 全局样式
- **Tailwind配置**: 支持深色模式切换

### 组件样式
- 使用Tailwind CSS utility classes
- 组件作用域样式
- 响应式设计支持

## 性能优化

### 代码分割
- 路由级别的懒加载
- 组件异步加载
- 第三方库按需引入

### 资源优化
- 图片懒加载
- Monaco Editor按需加载语言支持
- Vite构建优化配置

## 常见问题 (FAQ)

### Q: 如何添加新的工具视图？
A: 在 `src/components/toolViews/` 创建新组件，然后在 `ToolPanel.vue` 中注册。

### Q: 如何配置新的API端点？
A: 在 `src/api/` 相应文件中添加函数，更新类型定义，并在组件中调用。

### Q: 如何添加新的语言支持？
A: 在 `src/locales/` 添加新的语言文件，更新 `index.ts` 配置。

### Q: VNC连接失败怎么办？
A: 检查WebSocket连接、签名URL生成和沙箱服务状态。

## 相关文件清单

### 配置文件
- `package.json` - 项目依赖和脚本
- `tsconfig.json` - TypeScript配置
- `vite.config.ts` - Vite构建配置
- `tailwind.config.js` - Tailwind CSS配置
- `postcss.config.js` - PostCSS配置

### 源码目录结构
```
src/
├── api/           # API调用层
├── assets/        # 静态资源
├── components/    # Vue组件
├── composables/   # 组合式函数
├── constants/     # 常量定义
├── locales/       # 国际化文件
├── pages/         # 页面组件
├── types/         # TypeScript类型
├── utils/         # 工具函数
└── main.ts        # 应用入口
```

### 重要组件索引
- **认证相关**: `login/` 目录下的表单组件
- **聊天相关**: `ChatBox.vue`, `ChatMessage.vue`
- **工具相关**: `toolViews/` 目录下的各种工具视图
- **文件相关**: `FilePanel.vue`, `filePreviews/` 目录
- **设置相关**: `settings/` 目录下的配置组件

---

*本文档由AI自动生成，最后更新时间: 2025-11-04 13:13:53*