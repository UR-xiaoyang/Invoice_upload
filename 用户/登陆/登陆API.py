# 登陆API
from fastapi import APIRouter, HTTPException, Request

from 用户.登陆.用户登陆 import 用户登录
from 用户.登陆.登陆令牌 import 生成访问令牌
from 用户.登陆.登陆表单 import 登陆表单

登陆路由 = APIRouter()

@登陆路由.post("/登陆")
async def 登陆API(请求: Request, 表单: 登陆表单):
    用户登录(表单.用户名, 表单.密码, 请求.client.host)
    if 用户登录(表单.用户名, 表单.密码, 请求.client.host) == "密码错误，请重试。":
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    elif 用户登录(表单.用户名, 表单.密码, 请求.client.host) == "用户名错误，请重试。":
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    else:
        生成令牌 = 生成访问令牌(data={"sub": 表单.用户名})
        return {"access_token": 生成令牌, "token_type": "bearer"}
