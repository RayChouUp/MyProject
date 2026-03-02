# API 基础配置

## 1. 目录约定

```text
src/shared/api/
  http.js            # axios 实例 + 拦截器 + 错误处理
  request.js         # get/post/put/delete 统一封装
  modules/
    profile.js       # 业务接口模块示例
```

## 2. 环境变量

在项目根目录创建 `.env`（可参考 `.env.example`）：

- `VITE_API_BASE_URL`：后端 API 基础地址
- `VITE_API_TIMEOUT`：请求超时时间（毫秒）

示例：

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=10000
```

## 3. 拦截器行为

### 请求拦截

- 自动从 `localStorage.access_token` 读取 token
- 若 token 存在，自动添加请求头：`Authorization: Bearer <token>`

### 响应拦截

- 默认返回 `response.data`
- 若后端返回结构包含 `code` 字段，按以下规则处理：
  - `code === 0`：返回 `data`
  - `code !== 0`：抛出 `ApiError`

推荐后端返回结构：

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

## 4. 错误处理规则

统一抛出 `ApiError`，前端可通过 `try/catch` 捕获。

- 超时：`请求超时，请检查网络后重试`
- 无响应：`网络异常，请检查网络连接`
- HTTP 状态码：按内置映射转中文提示（如 401、404、500）

## 5. 使用示例

```js
import { fetchProfile, updateProfile } from './src/shared/api/modules/profile'

try {
  const profile = await fetchProfile()
  await updateProfile({ nickname: 'Alice' })
} catch (error) {
  console.error(error.message)
}
```
