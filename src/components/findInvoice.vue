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
      throw new Error('用户没有登录');
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
const selectedInvoices = ref<number[]>([]); // 复选框选中的发票ID列表

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
        content: item[1][8], // 内容
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

// OCR识别按钮API
const OCR = async (invoiceId: number) => {
  try {
    const token = getTokenFromCookie();
    if (!token) {
      throw new Error("Token没有发现");
    }

    // 发起 POST 请求，将发票ID发送给后端
    const response = await api.post('/ocr/OCR_server', {
      发票ID: invoiceId, // 使用 invoiceId 作为字段名称，而不是发票ID
    }, {
      headers: {
        Authorization: `Bearer ${token}`, // 将 token 添加到请求头中
        'Content-Type': 'application/json',
      },
    });

    // 弹窗提示
    if (response.data.status === 'success') {
      window.alert(`OCR处理成功：发票ID ${response.data.发票ID}`);
    } else {
      window.alert(`OCR处理失败：${response.data.message}`);
    }
  } catch (error) {
    console.error('OCR 处理出错：', error);
    window.alert('OCR 处理时发生错误。');
  }
};

// 批量OCR识别
const batchOCR = async () => {
  // 过滤出发票号码为 null 的发票
  const invoicesForOCR = invoiceData.value.filter(invoice =>
    selectedInvoices.value.includes(invoice.id) && invoice.number === null
  );

  if (invoicesForOCR.length === 0) {
    window.alert('无法进行OCR识别：选中的发票中没有符合条件的发票');
    return; // 阻止继续执行
  }

  // 创建一个数组用于存储所有OCR识别的Promise
  const ocrPromises = invoicesForOCR.map(invoice => OCR(invoice.id));

  try {
    // 并发所有OCR请求，使用 Promise.allSettled 来获取请求状态
    const 返回 = await Promise.allSettled(ocrPromises);

    // 处理每个OCR请求的结果
    返回.forEach((返回, index) => {
      if (返回.status === 'fulfilled') {
        console.log(`OCR成功：发票ID ${invoicesForOCR[index].id}`, 返回.value);
      } else {
        console.error(`OCR失败：发票ID ${invoicesForOCR[index].id}`, 返回.reason);
      }
    });

    // 显示完成信息
    window.alert('OCR识别已完成');


  } catch (error) {
    console.error('批量OCR处理过程中出错：', error);
    window.alert('批量OCR处理时发生错误，请联系管理员')
  }

};

// 全选或取消全选功能
const toggleSelectAll = (event: Event) => {
  const checked = (event.target as HTMLInputElement).checked;
  if (checked) {
    selectedInvoices.value = invoiceData.value.map(invoice => invoice.id); // 全选
  } else {
    selectedInvoices.value = []; // 全取消
  }
};

// 删除发票 API 方法
const del_invoice = async (invoiceID: number) => {
  try {
    const token = getTokenFromCookie();
    if (!token) {
      throw new Error("用户未登录");
    }

    // 发起 POST 请求，将发票 ID 发给后端
    const response = await api.post('/user/del_invoice', {
      ID: invoiceID,
    }, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    // 调试输出响应数据
    console.log("删除响应", response.data);

    // 删除弹窗
    if (response.data.code === 200) {
      console.log(`删除发票成功：${invoiceID}`);
      return response.data;
    } else {
      console.error(`删除发票失败：${response.data}`);
      return null;
    }
  } catch (error) {
    console.error('删除发票出错：', error);
    window.alert(`删除发票时发生错误, ${error.message}`);
    return null;
  }
};

// 批量删除选中发票
const 删除发票 = async () => {
  if (selectedInvoices.value.length === 0) {
    window.alert('没有选中发票');
    return;
  }

  // 遍历选中发票ID
  for (const invoiceID of selectedInvoices.value) {
    const 结果 = await del_invoice(invoiceID);
    if (结果) {
      // 删除成功即从本地删除该发票
      invoiceData.value = invoiceData.value.filter(invoice => invoice.id !== invoiceID);
    }
  }
  window.alert(`选中的发票已删除 ${selectedInvoices.value}`);
  // 清空选中的发票列表
  selectedInvoices.value = [];

}

</script>

<template>
  <div class="container">
    <!-- 标题和工具栏 -->
    <div class="header">
      <h1 class="title">发票查询</h1>
      <!-- 工具栏 -->
      <div class="toolbar">
        <input
          class="search-input"
          id="invoiceSearch"
          placeholder="请输入发票号码、发票代码、发票金额或上传日期"
          type="text"
        />
        <button class="search-button">查询</button>
        <button class="delete-button" @click="删除发票">批量删除</button>
        <button class="ocr-button" @click="batchOCR">批量OCR识别</button>
      </div>
    </div>

    <!-- 发票信息列表 -->
    <div class="invoice-list">
      <table class="invoice-table" v-if="invoiceData.length > 0">
        <thead>
        <tr>
          <th>
            <!-- 表头复选框点击全选/取消全选 -->
            <input type="checkbox" @change="toggleSelectAll" />
          </th>
          <th>ID</th>
          <th>发票号码</th>
          <th>发票代码</th>
          <th>发票类型</th>
          <th>金额</th>
          <th>日期</th>
          <th>内容</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="invoice in invoiceData" :key="invoice.id">
          <td>
            <!-- 每个发票记录前面的复选框 -->
            <input type="checkbox" v-model="selectedInvoices" :value="invoice.id" />
          </td>
          <td>{{ invoice.id }}</td>
          <td>{{ invoice.number }}</td>
          <td>{{ invoice.code }}</td>
          <td>{{ invoice.type }}</td>
          <td>{{ invoice.amount }}</td>
          <td>{{ invoice.date }}</td>
          <td>{{ invoice.content }}</td>
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
