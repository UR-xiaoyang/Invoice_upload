# 发票查询API
from fastapi import APIRouter, Request

from 用户.发票.发票查询.查询表单 import 发票查询表单
from 用户.发票.发票查询.用户发票查询 import 发票查询
from 用户.登陆.登陆令牌 import 验证令牌

发票查询路由器 = APIRouter()

@ 发票查询路由器.post("/发票查询")
async def 发票查询API(请求: Request, 表单: 发票查询表单):
    令牌 = 验证令牌(表单.token)
    if 令牌:
        IP = 请求.client.host
        查询数据 = 发票查询(表单.用户, 表单.页码, IP)
        if 查询数据:
            return {"code": 200, "msg": "查询成功", "data": 查询数据}
        else:
            return {"code": 400, "msg": "查询失败"}
    else:
        return {"code": 400, "msg": "登陆过期"}