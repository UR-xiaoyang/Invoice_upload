from fastapi import APIRouter, HTTPException, Request
from 用户.注册.注册表单 import 注册表单
from 用户.注册.注册验证 import 注册验证

注册路由 = APIRouter()

@注册路由.post("/注册")
async def 注册API(请求: Request, 表单: 注册表单):
    IP = 请求.client.host

    if 注册验证(表单.用户名, 表单.密码, 表单.邮箱, 表单.银行卡号, 表单.开户行, 表单.真实姓名, 表单.部门名称, IP):
        raise HTTPException(status_code=409, detail="用户名已存在")
    else:
        raise HTTPException(status_code=200, detail="注册成功")