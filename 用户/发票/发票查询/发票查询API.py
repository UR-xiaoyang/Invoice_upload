# 发票查询API
from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from 用户.发票.发票查询.查询发票数据 import 发票数据查询
from 用户.发票.发票查询.查询表单 import 发票查询表单
from 用户.发票.发票查询.用户发票查询 import 发票查询
from 用户.登陆.登陆令牌 import 验证令牌

发票查询路由器 = APIRouter()
security = HTTPBearer()

@ 发票查询路由器.post("/Invoice_Inquiry")
async def 发票查询API(请求: Request, 表单: 发票查询表单, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    令牌 = 验证令牌(token)
    if 令牌:
        
        IP = 请求.client.host
        查询数据 = 发票查询(令牌['sub'], 表单.页码, IP)
        发票数据 = 发票数据查询.获取数据(查询数据)
        if 发票数据:
            return {"code": 200, "msg": "查询成功", "data": 发票数据}
        else:
            return {"code": 400, "msg": "查询失败"}
    else:
        return {"code": 400, "msg": "登陆过期"}