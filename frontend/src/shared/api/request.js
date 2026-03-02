import http from './http'

export const get = (url, params = {}, config = {}) => http.get(url, { params, ...config })
export const post = (url, data = {}, config = {}) => http.post(url, data, config)
export const put = (url, data = {}, config = {}) => http.put(url, data, config)
export const del = (url, params = {}, config = {}) =>
  http.delete(url, {
    params,
    ...config,
  })

export { default as http } from './http'
