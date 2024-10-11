<script setup lang="ts">
import { api } from '@/API/API_connect';
import { onMounted, ref } from 'vue';
import * as XLSX from 'xlsx';


// 从 Cookie 中获取 token 的函数
const getTokenFromCookie = (): string | null => {
  const name = 'token=';
  const decodedCookie = decodeURIComponent(document.cookie);
  const cookiesArray = decodedCookie.split(';');

  for (let i = 0; i < cookiesArray.length; i++) {
    const cookie = cookiesArray[i].trim();
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

    const response = await api.post('/user/Invoice_Inquiry', {
      页码: queryParams.page,
    }, {
      headers: {
        Authorization: `Bearer ${token}`, // 将 token 添加到请求头中
        'Content-Type': 'application/json',
      },
    });

    return response.data;
  } catch (error) {
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

// 页面加载时调用查询
onMounted(async () => {
  try {
    const results = await searchInvoices({ page: 1 });
    invoiceData.value = parseInvoiceData(results.data);
    console.log(invoiceData.value);
  } catch (e) {
    console.error(e);
  }
});

// OCR完成识别后调用
const refreshInvoices = async () => {
  try {
    const results = await searchInvoices({ page: 1 });
    invoiceData.value = parseInvoiceData(results.data);
    console.log("发票数据已更新:", invoiceData.value);
  } catch (error) {
    console.error("重新请求发票数据时出错:", error);
    window.alert("刷新发票数据时发生错误，请重试");
  }
};

// OCR识别按钮API
const OCR = async (invoiceId: number) => {
  try {
    const token = getTokenFromCookie();
    if (!token) {
      throw new Error("Token没有发现");
    }

    const response = await api.post('/ocr/OCR_server', {
      发票ID: invoiceId,
    }, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

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
const batchOCR = async () => {
  const invoicesForOCR = invoiceData.value.filter(invoice =>
    selectedInvoices.value.includes(invoice.id) && invoice.number === null
  );

  if (invoicesForOCR.length === 0) {
    window.alert('无法进行OCR识别：选中的发票中没有符合条件的发票');
    return;
  }

  const ocrPromises = invoicesForOCR.map(invoice => OCR(invoice.id));

  try {
    const results = await Promise.allSettled(ocrPromises);

    results.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        console.log(`OCR成功：发票ID ${invoicesForOCR[index].id}`, result.value);
      } else {
        console.error(`OCR失败：发票ID ${invoicesForOCR[index].id}`, result.reason);
      }
    });

    window.alert('OCR识别已完成');

    // OCR 完成后重新查询发票信息
    await refreshInvoices();
  } catch (error) {
    console.error('批量OCR处理过程中出错：', error);
    window.alert('批量OCR处理时发生错误，请联系管理员');
  }
};


// 全选或取消全选功能
const toggleSelectAll = (event: Event) => {
  const checked = (event.target as HTMLInputElement).checked;
  if (checked) {
    selectedInvoices.value = invoiceData.value.map(invoice => invoice.id);

  } else {
    selectedInvoices.value = [];
  }
};

// 删除发票 API 方法
const delInvoice = async (invoiceID: number) => {
  try {
    const token = getTokenFromCookie();
    if (!token) {
      throw new Error("用户未登录");
    }

    const response = await api.post('/user/del_invoice', {
      ID: invoiceID,
    }, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

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

  for (const invoiceID of selectedInvoices.value) {
    const result = await delInvoice(invoiceID);
    if (result) {
      invoiceData.value = invoiceData.value.filter(invoice => invoice.id !== invoiceID);
    }
  }
  window.alert(`选中的发票已删除 ${selectedInvoices.value}`);
  selectedInvoices.value = [];
};

// 导出为Excel
const exportToExcel = () => {
  if (selectedInvoices.value.length === 0) {
    window.alert('没有可以导出的发票数据');
    return;
  }

  // 从 invoiceData 中找到选中的发票数据
  const selectedInvoiceData = invoiceData.value
    .filter(invoice => selectedInvoices.value.includes(invoice.id))
    .map(invoice => ({
      ID: invoice.id,
      发票号码: invoice.number,
      发票代码: invoice.code,
      发票类型: invoice.type,
      金额: invoice.amount,
      日期: invoice.date,
      内容: invoice.content,
    }));

  if (selectedInvoiceData.length === 0) {
    window.alert('没有可以导出的发票数据');
    return;
  }

  const worksheet = XLSX.utils.json_to_sheet(selectedInvoiceData);

  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "发票数据");

  const data = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
  const blob = new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

  const link = document.createElement('a');
  link.href = window.URL.createObjectURL(blob);
  link.download = '发票数据.xlsx';
  link.click();
};

// 发票下载
const invoiceDownload = async (): Promise<void> => {
  // 从Cookie中获取token
  const token = getTokenFromCookie();
  if (!token) {
    window.alert("用户未登录，无法下载发票");
    return;
  }

  // 检查是否有选中的发票ID
  if (selectedInvoices.value.length === 0) {
    window.alert("请至少选择一个发票进行下载");
    return;
  }

  try {
    // 显示下载开始的提示
    window.alert(`开始下载发票: ${selectedInvoices.value.join(', ')}`);

    // 发票ID数组直接传递到API请求中，符合API要求的数组格式 [88, 89]
    const response = await api.post('/user/DownZIP', selectedInvoices.value, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Accept': 'application/zip', // 请求接收zip文件
      },
      responseType: 'blob', // 将响应类型设置为 blob 以便处理二进制数据
    });

    // 如果请求成功，处理下载文件
    const blob = new Blob([response.data], { type: 'application/zip' });
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = 'invoices.zip'; // 设置下载文件名
    link.click();

    // 成功提示
    window.alert("发票下载成功");
    console.log(`下载发票成功：${selectedInvoices.value}`);
  } catch (error) {
    // 错误处理
    console.error('下载发票出错：', error);
    window.alert(`下载发票时发生错误, 错误信息: ${error.message}`);
  }
};


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
        <button class="excel-button" @click="exportToExcel">导出Excel</button>
        <button class="download-invoice" @click="invoiceDownload">下载发票</button>
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
.excel-button {
  background-color: #28a745; /* 绿色背景，表示成功/导出 */
  color: white; /* 白色文字 */
  padding: 10px 20px; /* 按钮内边距 */
  border: none; /* 去除默认边框 */
  border-radius: 5px; /* 圆角 */
  font-size: 16px; /* 字体大小 */
  font-weight: bold; /* 字体加粗 */
  cursor: pointer; /* 鼠标悬停时变为手指 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 按钮阴影 */
  transition: background-color 0.3s, box-shadow 0.3s; /* 动画过渡 */
}

.excel-button:hover {
  background-color: #218838; /* 鼠标悬停时背景变深 */
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15); /* 悬停时加深阴影 */
}

.excel-button:active {
  background-color: #1e7e34; /* 点击时背景变得更深 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* 点击时阴影减小 */
}


.download-invoice {
  padding: 10px 20px;
  font-size: 16px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.download-invoice:hover {
  background-color: #0056b3;
}

</style>
