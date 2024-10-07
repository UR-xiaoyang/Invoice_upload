from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from 发票处理.删除.删除发票 import DeleteInvoice
from 发票处理.删除.删除表单 import DeleteInvoice_label
from 用户.登陆.登陆令牌 import 验证令牌

# 创建 APIRouter 实例
删除发票路由 = APIRouter()
security = HTTPBearer()

# 删除发票的路由
@删除发票路由.post("/del_invoice")
async def 删除发票(
    表单: DeleteInvoice_label,
    请求: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # 从 HTTP 头中提取 token
    token = credentials.credentials
    # 获取客户端 IP 地址
    IP = 请求.client.host

    # 验证 token
    验证 = 验证令牌(token)
    if not 验证:
        # 如果验证失败，抛出 401 Unauthorized 错误
        raise HTTPException(status_code=401, detail="Token验证失败")

    # 调用删除函数，传入发票ID、客户端IP、操作人ID
    删除结果 = DeleteInvoice.Delete(表单.ID, IP, 验证['sub'])
    if 删除结果:
        # 删除成功，返回200状态码和成功消息
        return {"code": 200, "msg": "删除成功"}
    else:
        # 删除失败，抛出 422 Unprocessable Entity 错误
        raise HTTPException(status_code=422, detail="删除失败")
