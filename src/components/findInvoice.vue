<script setup lang="ts">
import { api } from '@/API/API_connect';
import { onMounted, ref } from 'vue';

// 从 Cookie 中获取 token 的函数
const getTokenFromCookie = (): string | null => {
  const name = 'token=';
  const decodedCookie = decodeURIComponent(document.cookie);
  const cookiesArray = decodedCookie.split(';');

  for (let i = 0; i < cookiesArray.length; i++) {
    let cookie = cookiesArray[i].trim();
    if (cookie.indexOf(name) === 0) {
      return cookie.substring(name.length, cookie.length);
    }
  }
  return null; // 如果没有找到 token 则返回 null
};

// 查询发票信息的 API 请求函数 (POST 请求)
const searchInvoices = async (queryParams: { page: number }) => {
  try {
    const token = getTokenFromCookie(); // 从 Cookie 中获取 token

    if (!token) {
      throw new Error('Token not found in cookies');
    }

    // 发起 POST 请求，并将用户输入的查询条件作为请求体
    const response = await api.post('/user/Invoice_Inquiry', {
      页码: queryParams.page,
    }, {
      headers: {
        Authorization: `Bearer ${token}`, // 将 token 添加到请求头中
        'Content-Type': 'application/json',
      },
    });

    // 返回成功响应
    return response.data;
  } catch (error) {
    // 错误处理
    console.error('发票查询出错:', error);
    throw error; // 将错误抛出以便在调用处处理
  }
};

// 存储查询结果
const invoiceData = ref<any[]>([]);

// 解析返回数据，保留 `null` 数据
const parseInvoiceData = (data: any[]) => {
  return data.map((item) => {
    if (item[1] === null) {
      return {
        id: item[0], // 只返回ID，其他字段为 null
        number: null,
        code: null,
        type: null,
        amount: null,
        date: null,
      };
    } else {
      return {
        id: item[0], // 发票ID
        number: item[1][2], // 发票号码
        code: item[1][3], // 发票代码
        type: item[1][6], // 发票类型
        amount: item[1][4], // 金额
        date: item[1][7], // 日期
      };
    }
  });
};

// 加载调用
onMounted(async () => {
  try {
    // 页面加载自动调用查询，页码为1
    const results = await searchInvoices({ page: 1 });
    // 解析并赋值查询结果，保留 `null`
    invoiceData.value = parseInvoiceData(results.data);
    console.log(invoiceData.value); // 打印结果用于调试
  } catch (e) {
    console.log(e);
  }
});
</script>

<template>
  <div class="container">
    <!-- 标题和搜索框 -->
    <div class="header">
      <h1 class="title">发票查询</h1>
      <div class="search-area">
        <input
          class="search-input"
          id="invoiceSearch"
          placeholder="请输入发票号码、发票代码、发票金额或上传日期"
          type="text"
        />
        <button class="search-button">查询</button>
        <!-- 分页功能 -->
        <div class="pagination">
          <button class="pagination-button">上一页</button>
          <span class="page-info">第 1 页，共 10 页</span>
          <button class="pagination-button">下一页</button>
        </div>
      </div>
    </div>

    <!-- 发票信息列表 -->
    <div class="invoice-list">
      <table class="invoice-table" v-if="invoiceData.length > 0">
        <thead>
        <tr>
          <th>ID</th>
          <th>发票号码</th>
          <th>发票代码</th>
          <th>发票类型</th>
          <th>金额</th>
          <th>日期</th>
          <th>操作</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="invoice in invoiceData" :key="invoice.id">
          <td>{{ invoice.id }}</td>
          <td>{{ invoice.number }}</td>
          <td>{{ invoice.code }}</td>
          <td>{{ invoice.type }}</td>
          <td>{{ invoice.amount }}</td>
          <td>{{ invoice.date }}</td>
          <td>
            <!-- 只有当发票数据为 null 时显示 OCR 识别按钮 -->
            <button v-if="invoice.number === null" class="ocr-button">OCR 识别</button>
            <button class="delete-button">删除</button>
          </td>
        </tr>
        <!-- 更多发票信息行 -->
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
@import url(../assets/findInvoice.css);

/* 你可以根据需要调整CSS样式 */
</style>
