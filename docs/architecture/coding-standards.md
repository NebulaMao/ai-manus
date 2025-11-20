# AI Manus 编码规范

## 📋 文档信息

| 属性 | 值 |
|------|-----|
| **项目名称** | AI Manus - 通用AI Agent系统 |
| **规范版本** | v1.0 |
| **创建日期** | 2025-11-05 |
| **适用范围** | 全项目 (Frontend + Backend + Sandbox) |
| **语言** | 中文 |

---

## 🚀 概述

本文档定义了 AI Manus 项目的统一编码规范，确保代码质量、可维护性和团队协作效率。规范涵盖前端 (Vue 3 + TypeScript)、后端 (FastAPI + Python) 和基础设施配置。

### 核心原则

1. **KISS (Keep It Simple, Stupid)** - 保持代码简单明了
2. **DRY (Don't Repeat Yourself)** - 避免代码重复
3. **SOLID** - 遵循面向对象设计原则
4. **YAGNI (You Aren't Gonna Need It)** - 不过度设计
5. **可读性优先** - 代码首先是写给人看的

---

## 🎨 通用编码规范

### 文件命名规范

| 类型 | 命名规范 | 示例 |
|------|----------|------|
| 组件文件 | PascalCase | `UserProfile.vue` |
| 工具文件 | camelCase | `userUtils.ts` |
| 配置文件 | kebab-case | `docker-compose.yml` |
| Python文件 | snake_case | `user_service.py` |
| 常量文件 | UPPER_SNAKE | `API_CONSTANTS.ts` |

### 目录结构规范

```
src/
├── components/          # 组件目录 (PascalCase)
│   ├── common/         # 通用组件
│   ├── forms/          # 表单组件
│   └── layout/         # 布局组件
├── composables/        # 组合式函数 (camelCase)
├── services/           # API服务层 (camelCase)
├── stores/             # 状态管理 (camelCase)
├── utils/              # 工具函数 (camelCase)
├── types/              # 类型定义 (camelCase)
└── styles/             # 样式文件 (camelCase)
```

### 注释规范

#### 1. 文件头注释
```typescript
/**
 * @fileoverview 用户认证服务
 * @author 开发者姓名
 * @created 2025-11-05
 * @updated 2025-11-05
 */
```

#### 2. 函数注释
```typescript
/**
 * 用户登录验证
 * @param credentials 登录凭据
 * @returns Promise<User> 用户信息
 * @throws UnauthorizedError 认证失败
 */
async function login(credentials: LoginCredentials): Promise<User>
```

#### 3. 复杂逻辑注释
```typescript
// 检查用户权限：管理员或资源所有者
const hasPermission = user.role === 'admin' || user.id === resource.ownerId
```

---

## 🖥️ 前端编码规范 (Vue 3 + TypeScript)

### TypeScript 规范

#### 1. 类型定义
```typescript
// 优先使用 interface 定义对象类型
interface User {
  id: string
  username: string
  email: string
  role: UserRole
}

// 使用 type 定义联合类型或复杂类型
type UserRole = 'admin' | 'user' | 'guest'
type ApiResponse<T> = {
  data: T
  message: string
  success: boolean
}
```

#### 2. 严格类型检查
```typescript
// ✅ 正确：明确的类型定义
const users: User[] = []

// ❌ 错误：使用 any
const users: any[] = []

// ✅ 正确：使用泛型
const apiResponse = await fetchData<User>('/api/users')
```

#### 3. 枚举使用
```typescript
// 使用字符串枚举
enum TaskStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed'
}
```

### Vue 3 组件规范

#### 1. 组件结构
```vue
<template>
  <!-- 模板内容：使用语义化标签，合理的缩进 -->
  <section class="user-profile">
    <header class="profile-header">
      <h2>{{ user.username }}</h2>
    </header>
    <main class="profile-content">
      <!-- 内容区域 -->
    </main>
  </section>
</template>

<script setup lang="ts">
// 1. 导入语句
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import type { User } from '@/types/user'

// 2. Props 定义
interface Props {
  userId: string
  showDetails?: boolean
}
const props = withDefaults(defineProps<Props>(), {
  showDetails: true
})

// 3. Emits 定义
interface Emits {
  update: [user: User]
  delete: [userId: string]
}
const emit = defineEmits<Emits>()

// 4. 响应式数据
const user = ref<User | null>(null)
const loading = ref(false)

// 5. 计算属性
const isAdmin = computed(() => user.value?.role === 'admin')

// 6. 方法
const fetchUser = async () => {
  loading.value = true
  try {
    // 业务逻辑
  } finally {
    loading.value = false
  }
}

// 7. 生命周期
onMounted(() => {
  fetchUser()
})
</script>

<style scoped>
/* 样式：使用 scoped 避免污染 */
.user-profile {
  @apply p-4 border rounded-lg;
}

.profile-header {
  @apply mb-4;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-profile {
    @apply p-2;
  }
}
</style>
```

#### 2. Composition API 规范
```typescript
// composables/useAuth.ts
import { ref, computed } from 'vue'
import { authApi } from '@/services/auth'
import type { User, LoginCredentials } from '@/types/user'

export function useAuth() {
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  const login = async (credentials: LoginCredentials) => {
    loading.value = true
    error.value = null

    try {
      const response = await authApi.login(credentials)
      user.value = response.user
      return response
    } catch (err) {
      error.value = err instanceof Error ? err.message : '登录失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    user.value = null
    error.value = null
  }

  return {
    // 状态
    user: readonly(user),
    loading: readonly(loading),
    error: readonly(error),

    // 计算属性
    isAuthenticated,
    isAdmin,

    // 方法
    login,
    logout
  }
}
```

### CSS/样式规范

#### 1. Tailwind CSS 优先
```vue
<template>
  <!-- ✅ 优先使用 Tailwind 类 -->
  <div class="flex items-center justify-between p-4 bg-white rounded-lg shadow">
    <!-- 内容 -->
  </div>

  <!-- ❌ 避免内联样式 -->
  <div style="display: flex; padding: 16px;">
    <!-- 内容 -->
  </div>
</template>
```

#### 2. 组件样式组织
```vue
<style scoped>
/* 1. 布局样式 */
.container {
  @apply max-w-4xl mx-auto p-4;
}

/* 2. 组件特定样式 */
.button-primary {
  @apply px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600;
}

/* 3. 状态样式 */
.is-active {
  @apply border-blue-500 bg-blue-50;
}

/* 4. 响应式样式 */
@media (max-width: 768px) {
  .container {
    @apply px-2;
  }
}

/* 5. 动画样式 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
</style>
```

---

## 🐍 后端编码规范 (FastAPI + Python)

### Python 基础规范

#### 1. 代码格式化
```python
# 使用 Black 进行代码格式化
# 行长度限制：88 字符
# 使用双引号字符串

# ✅ 正确格式
async def create_user(user_data: UserCreate) -> User:
    """创建新用户"""
    user = User(**user_data.dict())
    await user.insert()
    return user

# ❌ 错误格式
async def create_user(user_data: UserCreate)->User:
    """创建新用户"""
    user=User(**user_data.dict())
    await user.insert()
    return user
```

#### 2. 导入语句规范
```python
# 标准库导入
import asyncio
from datetime import datetime
from typing import List, Optional

# 第三方库导入
from fastapi import APIRouter, Depends, HTTPException
from beanie import Document, Indexed
from pydantic import BaseModel

# 本地导入
from app.domain.models.user import User
from app.infrastructure.mongodb.database import get_database
from app.interfaces.api.dependencies import get_current_user
```

### FastAPI 应用规范

#### 1. 路由定义
```python
# interfaces/api/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.domain.models.user import User
from app.domain.services.user_service import UserService
from app.interfaces.schemas.user import UserCreate, UserResponse, UserUpdate
from app.interfaces.api.dependencies import get_current_user, get_user_service

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> List[User]:
    """
    获取用户列表

    - **skip**: 跳过记录数
    - **limit**: 返回记录数限制
    - **current_user**: 当前认证用户
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )

    return await user_service.get_users(skip=skip, limit=limit)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> User:
    """创建新用户"""
    try:
        return await user_service.create_user(user_data.dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

#### 2. Pydantic 模型规范
```python
# interfaces/schemas/user.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str = "user"

class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度至少8位')
        return v

    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError('用户名只能包含字母和数字')
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None

class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str
```

#### 3. 服务层规范
```python
# domain/services/user_service.py
from typing import List, Optional
from datetime import datetime

from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.auth import SecurityService

class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        security_service: SecurityService
    ):
        self.user_repository = user_repository
        self.security_service = security_service

    async def create_user(self, user_data: dict) -> User:
        """创建新用户"""
        # 检查用户名是否已存在
        existing_user = await self.user_repository.get_by_username(
            user_data['username']
        )
        if existing_user:
            raise ValueError("用户名已存在")

        # 检查邮箱是否已存在
        existing_email = await self.user_repository.get_by_email(
            user_data['email']
        )
        if existing_email:
            raise ValueError("邮箱已存在")

        # 哈希密码
        user_data['password_hash'] = self.security_service.hash_password(
            user_data.pop('password')
        )

        # 创建用户
        user = User(**user_data)
        user.created_at = datetime.utcnow()
        user.updated_at = datetime.utcnow()

        return await self.user_repository.create(user)

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        """用户认证"""
        user = await self.user_repository.get_by_username(username)

        if not user or not user.is_active:
            return None

        if not self.security_service.verify_password(password, user.password_hash):
            return None

        return user

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """获取用户列表"""
        return await self.user_repository.get_multi(skip=skip, limit=limit)
```

### 数据库模型规范

#### 1. Beanie ODM 模型
```python
# domain/models/user.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from beanie import Document, Indexed

class User(Document):
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    password_hash: str
    role: str = "user"
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    last_login: Optional[datetime] = None

    class Settings:
        name = "users"
        indexes = [
            "username",
            "email",
            "role",
            "is_active",
            "created_at"
        ]

    @validator('role')
    def validate_role(cls, v):
        allowed_roles = ['admin', 'user', 'guest']
        if v not in allowed_roles:
            raise ValueError(f'角色必须是以下之一: {allowed_roles}')
        return v

    def update_last_login(self):
        """更新最后登录时间"""
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()
```

#### 2. Repository 模式
```python
# domain/repositories/user_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from beanie import PydanticObjectId

from app.domain.models.user import User

class UserRepository(ABC):
    """用户仓储接口"""

    @abstractmethod
    async def create(self, user: User) -> User:
        """创建用户"""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """根据ID获取用户"""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        pass

    @abstractmethod
    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[User]:
        """获取用户列表"""
        pass

    @abstractmethod
    async def update(self, user_id: str, update_data: dict) -> Optional[User]:
        """更新用户"""
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """删除用户"""
        pass

# infrastructure/mongodb/repositories/user_repository.py
from typing import List, Optional
from beanie import PydanticObjectId

from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository

class MongoUserRepository(UserRepository):
    """MongoDB 用户仓储实现"""

    async def create(self, user: User) -> User:
        return await user.insert()

    async def get_by_id(self, user_id: str) -> Optional[User]:
        return await User.get(PydanticObjectId(user_id))

    async def get_by_username(self, username: str) -> Optional[User]:
        return await User.find_one(User.username == username)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await User.find_one(User.email == email)

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await User.find().skip(skip).limit(limit).to_list()

    async def update(self, user_id: str, update_data: dict) -> Optional[User]:
        user = await User.get(PydanticObjectId(user_id))
        if user:
            for key, value in update_data.items():
                setattr(user, key, value)
            user.updated_at = datetime.utcnow()
            await user.save()
        return user

    async def delete(self, user_id: str) -> bool:
        user = await User.get(PydanticObjectId(user_id))
        if user:
            await user.delete()
            return True
        return False
```

---

## 🔧 配置和基础设施规范

### 环境变量规范

#### 1. 命名规范
```bash
# 使用大写字母和下划线
# 按功能分组，使用相同前缀

# 数据库配置
MONGODB_URL=mongodb://localhost:27017/ai_manus
REDIS_URL=redis://localhost:6379/0

# API配置
API_BASE=http://localhost:8000
API_SECRET_KEY=your-secret-key-here

# 外部服务
OPENAI_API_KEY=your-openai-key
OPENAI_BASE_URL=https://api.openai.com/v1

# Docker配置
DOCKER_HOST=unix:///var/run/docker.sock
SANDBOX_NETWORK=ai-manus-sandbox
```

#### 2. 配置管理
```python
# app/core/config.py
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "AI Manus"
    debug: bool = False
    version: str = "1.0.0"

    # 数据库配置
    mongodb_url: str
    redis_url: str

    # 安全配置
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # 外部API
    openai_api_key: Optional[str] = None
    openai_base_url: str = "https://api.openai.com/v1"

    # Docker配置
    docker_host: str = "unix:///var/run/docker.sock"
    sandbox_network: str = "ai-manus-sandbox"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

### Docker 规范

#### 1. Dockerfile 规范
```dockerfile
# 使用多阶段构建
FROM python:3.10-slim as builder

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 生产阶段
FROM python:3.10-slim

WORKDIR /app

# 复制安装的依赖
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 复制应用代码
COPY . .

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Docker Compose 规范
```yaml
version: '3.8'

services:
  # 后端服务
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongodb:27017/ai_manus
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - mongodb
      - redis
    volumes:
      - ./backend:/app
    restart: unless-stopped
    networks:
      - ai-manus-network

  # 前端服务
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "5173:5173"
    environment:
      - VITE_API_BASE_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    restart: unless-stopped
    networks:
      - ai-manus-network

  # 数据库服务
  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped
    networks:
      - ai-manus-network

  # 缓存服务
  redis:
    image: redis:7.0-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - ai-manus-network

volumes:
  mongodb_data:
  redis_data:

networks:
  ai-manus-network:
    driver: bridge
```

---

## 🧪 测试规范

### 测试文件组织

```
tests/
├── unit/                   # 单元测试
│   ├── frontend/          # 前端单元测试
│   │   ├── components/    # 组件测试
│   │   ├── composables/   # 组合式函数测试
│   │   └── utils/         # 工具函数测试
│   └── backend/           # 后端单元测试
│       ├── services/      # 服务层测试
│       ├── repositories/  # 数据层测试
│       └── utils/         # 工具函数测试
├── integration/           # 集成测试
│   ├── api/              # API集成测试
│   └── database/         # 数据库集成测试
└── e2e/                  # 端到端测试
    ├── auth.spec.ts      # 认证流程测试
    └── agents.spec.ts    # Agent管理测试
```

### 测试命名规范

```typescript
// frontend/tests/unit/components/UserCard.spec.ts
describe('UserCard', () => {
  describe('when user is admin', () => {
    it('should display admin badge', () => {
      // 测试实现
    })
  })

  describe('when user is regular user', () => {
    it('should not display admin badge', () => {
      // 测试实现
    })
  })
})
```

```python
# backend/tests/unit/services/test_user_service.py
class TestUserService:
    def test_create_user_success(self, user_service, user_data):
        """测试成功创建用户"""
        user = await user_service.create_user(user_data)

        assert user.username == user_data['username']
        assert user.email == user_data['email']
        assert user.id is not None

    def test_create_user_duplicate_username(self, user_service, user_data):
        """测试创建重复用户名用户"""
        await user_service.create_user(user_data)

        with pytest.raises(ValueError, match="用户名已存在"):
            await user_service.create_user(user_data)
```

---

## 📏 代码质量检查

### 工具配置

#### 1. ESLint + Prettier (Frontend)
```json
// .eslintrc.json
{
  "extends": [
    "@vue/typescript/recommended",
    "@vue/prettier",
    "@vue/prettier/@typescript-eslint"
  ],
  "rules": {
    "no-console": "warn",
    "no-debugger": "error",
    "@typescript-eslint/no-unused-vars": "error",
    "vue/component-name-in-template-casing": ["error", "PascalCase"],
    "vue/prop-name-casing": ["error", "camelCase"]
  }
}
```

```json
// .prettierrc
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "none",
  "printWidth": 88,
  "endOfLine": "lf"
}
```

#### 2. Black + MyPy (Backend)
```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'
extend-exclude = '''
/(
  migrations
)/
'''

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
```

### Git Hooks 配置

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black
        files: ^backend/

  - repo: https://github.com/pycqa/isort
    rev: 5.11.4
    hooks:
      - id: isort
        files: ^backend/

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.991
    hooks:
      - id: mypy
        files: ^backend/
        additional_dependencies: [types-all]

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.30.0
    hooks:
      - id: eslint
        files: ^frontend/
        types: [file]
        types_or: [javascript, jsx, ts, tsx, vue]
```

---

## 📝 提交规范

### Conventional Commits

```bash
# 提交格式
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### 提交类型
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

#### 示例
```bash
feat(auth): add user login functionality

- Implement login API endpoint
- Add JWT token generation
- Create login form component

Closes #123
```

```bash
fix(api): resolve user creation validation error

- Fix email validation regex
- Add proper error handling

Closes #124
```

---

## 🔄 代码审查清单

### 提交前检查

- [ ] 代码符合项目编码规范
- [ ] 所有测试通过
- [ ] 添加了必要的测试用例
- [ ] 更新了相关文档
- [ ] 没有硬编码的配置信息
- [ ] 错误处理完善
- [ ] 性能影响可接受
- [ ] 安全性考虑充分

### 审查要点

#### 1. 代码质量
- 逻辑清晰易懂
- 函数职责单一
- 没有重复代码
- 命名规范合理

#### 2. 架构一致性
- 遵循现有架构模式
- 正确使用设计模式
- 模块间依赖合理

#### 3. 性能考虑
- 数据库查询优化
- 缓存策略合理
- 资源使用高效

#### 4. 安全性
- 输入验证完整
- 权限检查到位
- 敏感信息保护

---

## 📚 参考资源

### 官方文档
- [Vue 3 文档](https://vuejs.org/)
- [TypeScript 文档](https://www.typescriptlang.org/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Python PEP 8](https://peps.python.org/pep-0008/)

### 工具文档
- [ESLint 规则](https://eslint.org/docs/rules/)
- [Prettier 配置](https://prettier.io/docs/en/options.html)
- [Black 配置](https://black.readthedocs.io/en/stable/)
- [MyPy 配置](https://mypy.readthedocs.io/en/stable/config_file.html)

### 最佳实践
- [Vue 3 Style Guide](https://vuejs.org/style-guide/)
- [TypeScript Best Practices](https://typescript-eslint.io/rules/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/best-practices/)

---

## 📝 文档维护

### 更新频率
- 每月检查和更新
- 新技术引入时及时更新
- 团队反馈后持续改进

### 贡献指南
1. 发现规范不合理的地方，及时提出改进建议
2. 新增技术栈时，补充相应的编码规范
3. 定期分享最佳实践和经验教训

---

*本文档由 AI 自动生成，遵循 AI Manus 项目编码规范*
*最后更新时间: 2025-11-05*