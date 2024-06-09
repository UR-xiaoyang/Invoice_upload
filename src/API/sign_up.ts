// 用户注册数据接口定义
export interface 用户注册表单 {
  用户名: string;
  密码: string;
  邮箱: string;
  银行卡号: string;
  开户行: string;
  真实姓名: string;
  部门名称: string;
}

// API路径配置
const API_CONFIG = {
  用户注册: 'http://localhost:8000',
};

/**
 * 提交用户注册信息至服务器
 *
 * @param data 用户注册表单数据
 * @returns 注册操作的响应结果
 */
export const 提交用户注册 = async (data: 用户注册表单): Promise<any> => {
  try {
    // 发起POST请求进行用户注册
    const response = await api.post(API_CONFIG.用户注册, data);
    return response.data;
  } catch (error) {
    // 记录错误信息
    console.error('用户注册时发生错误:', error.message);

    // 根据错误响应细化处理逻辑
    if (error.response && error.response.status === 400) {
      console.error('提交的注册信息有误');
    }

    // 重新抛出错误，允许外部调用者进一步处理
    throw error;
  }
};
