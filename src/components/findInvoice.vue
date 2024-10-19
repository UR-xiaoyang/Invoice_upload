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
const Identify_server = async (invoiceId: number, isOCR: boolean) => {
  try {
    const token = getTokenFromCookie();
    if (!token) {
      throw new Error('Token没有发现');
    }

    const response = await api.post('/user/Identify_server', {
      发票ID: invoiceId,
      OCR: isOCR, // 添加 OCR 参数
    }, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (response.data.status === 'success') {
      window.alert(`识别成功：发票ID ${response.data.发票ID}`);
    } else {
      window.alert(`识别失败：${response.data.message}`);
    }
  } catch (error) {
    console.error('识别出错：', error);
    window.alert('识别时发生错误。');
  }
};


const Identify = async (isOCR: boolean) => {
  // 筛选出符合条件的发票
  const invoicesForOCR = invoiceData.value.filter(invoice =>
    selectedInvoices.value.includes(invoice.id) && invoice.number === null
  );

  if (invoicesForOCR.length === 0) {
    window.alert('无法进行识别：选中的发票中没有符合条件的发票');
    return;
  }

  // 收集所有 OCR 请求的 Promise，传递 OCR 参数
  const ocrPromises = invoicesForOCR.map(invoice =>
    Identify_server(invoice.id, isOCR)
  );

  try {
    const results = await Promise.allSettled(ocrPromises);

    const successInvoices = [];
    const failedInvoices = [];

    results.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        successInvoices.push(invoicesForOCR[index].id);
        console.log(`识别成功：发票ID ${invoicesForOCR[index].id}`, result.value);
      } else {
        failedInvoices.push(invoicesForOCR[index].id);
        console.error(`识别失败：发票ID ${invoicesForOCR[index].id}`, result.reason);
      }
    });

    let alertMessage = `识别已完成。\n`;
    if (successInvoices.length > 0) {
      alertMessage += `成功的发票ID：${successInvoices.join(', ')}\n`;
    }
    if (failedInvoices.length > 0) {
      alertMessage += `失败的发票ID：${failedInvoices.join(', ')}\n请重试。`;
    }

    window.alert(alertMessage);

    await refreshInvoices(); // 刷新发票数据
  } catch (error) {
    console.error('批量识别过程中出错：', error);
    window.alert('批量识别时发生错误，请联系管理员');
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

//
</script>

<template>
  <div class="bg">
    <div class="container">
      <!-- 标题和工具栏 -->
      <div class="header">
        <h1 class="title">发票管理</h1>
        <!-- 工具栏 -->
        <div class="toolbar">

          <button class="delete-button" @click="删除发票">批量删除</button>
          <button class="quick-identify-button" @click="Identify(false)">快速识别</button>
          <button class="ocr-identify-button" @click="Identify(true)">OCR识别</button>
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
  </div>
</template>

<style scoped>
@import url(../assets/findInvoice.css);

</style>
