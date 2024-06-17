from typing import List
from fastapi import APIRouter, UploadFile, File, Request, Depends

from 数据库.日志.log表 import 记录日志
from 用户.发票.发票上传.发票上传 import 存储发票
from 用户.登陆.登陆令牌 import 验证令牌

发票上传路由 = APIRouter()

@发票上传路由.post("/upload_invoice")
async def 发票上传API(
    请求: Request,
    upload_file: List[UploadFile] = File(...)
):
    验证结果 = 验证令牌(请求.cookies.get("token"))
    if 验证结果:
        # 获取IP
        IP = 请求.client.host
        for 文件index in range(len(upload_file)):
            存储发票(upload_file[文件index], 验证结果['sub'], IP)
        return {"code": 200, "msg": "上传成功"}
    else:
        return {"code": 400, "msg": "登陆过期"}
