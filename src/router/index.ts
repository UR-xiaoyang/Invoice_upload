import { createRouter, createWebHistory } from 'vue-router'
import UploadInvoice from '../components/UploadInvoice.vue'
import sign_up from '../components/sign_up.vue'
import sign_in from '../components/sign_in.vue'
// 路由页面
const routes = [
  {
    // 上传页面（主页）
    path: '/',
    name: 'upload_invoice',
    component: UploadInvoice
  },
  {
    path: '/sign_up',
    name: 'sign_up',
    component: sign_up
  },
  {
    path: '/sign_in',
    name: 'sign_in',
    component: sign_in
  }

]
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router
