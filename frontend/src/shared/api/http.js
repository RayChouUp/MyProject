import axios from 'axios'

const DEFAULT_TIMEOUT = 10000

const HTTP_STATUS_MESSAGE = {
  400: '请求参数错误',
  401: '登录状态已失效，请重新登录',
  403: '没有权限访问该资源',
  404: '请求资源不存在',
  408: '请求超时，请稍后重试',
  429: '请求过于频繁，请稍后再试',
  500: '服务器开小差了，请稍后重试',
  502: '网关错误，请稍后重试',
  503: '服务暂不可用，请稍后重试',
  504: '网关超时，请稍后重试',
}

const createApiError = (message, extra = {}) => {
  const error = new Error(message)
  error.name = 'ApiError'
  Object.assign(error, extra)
  return error
}

const getAuthToken = () => localStorage.getItem('access_token')

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: Number(import.meta.env.VITE_API_TIMEOUT || DEFAULT_TIMEOUT),
  headers: {
    'Content-Type': 'application/json',
  },
})

http.interceptors.request.use(
  (config) => {
    const token = getAuthToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(createApiError('请求配置错误', { cause: error })),
)

http.interceptors.response.use(
  (response) => {
    const payload = response?.data

    if (payload && typeof payload === 'object' && 'code' in payload) {
      if (payload.code !== 0) {
        return Promise.reject(
          createApiError(payload.message || '业务处理失败', {
            code: payload.code,
            data: payload.data,
            response,
          }),
        )
      }
      return payload.data
    }

    return payload
  },
  (error) => {
    if (error.code === 'ECONNABORTED') {
      return Promise.reject(createApiError('请求超时，请检查网络后重试', { cause: error }))
    }

    if (!error.response) {
      return Promise.reject(createApiError('网络异常，请检查网络连接', { cause: error }))
    }

    const status = error.response.status
    const message = HTTP_STATUS_MESSAGE[status] || `请求失败（${status}）`
    return Promise.reject(
      createApiError(message, {
        status,
        response: error.response,
        cause: error,
      }),
    )
  },
)

export default http
