import axios from 'axios';

// 动态获取 API 地址，默认为 'http://127.0.0.1:8000'
const apiBaseUrl = window.API_CONFIG?.BASE_URL || 'http://127.0.0.1:8000';

// 创建一个 axios 实例
export const api = axios.create({
  baseURL: apiBaseUrl, // 使用动态配置的 API 地址
  timeout: 100000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json',
  },
});

// 添加请求拦截器
api.interceptors.request.use(config => {
  // 根据后端要求，可能需要添加特定的请求头
  config.headers['X-Requested-With'] = 'XMLHttpRequest'; // 示例，根据实际情况调整

  return config;
}, error => {
  return Promise.reject(error);
});
