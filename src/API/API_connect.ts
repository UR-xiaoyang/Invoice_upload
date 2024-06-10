import axios from 'axios';

// 创建一个 axios 实例
export const api = axios.create({
  baseURL: 'http://localhost:8000/', // 后端 API 的基础 URL
  timeout: 1000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json',
  },
});

// 添加请求拦截器
api.interceptors.request.use(config => {
  // 根据后端要求，可能需要添加特定的请求头
  config.headers['X-Requested-With'] = 'XMLHttpRequest'; // 示例，根据实际情况调整

  // 如果后端需要特定的预检请求头，这里可以添加
  // 注意：通常不需要手动设置，除非后端有特殊要求
  // config.headers['Access-Control-Request-Headers'] = 'Content-Type';

  return config;
}, error => {
  return Promise.reject(error);
});
