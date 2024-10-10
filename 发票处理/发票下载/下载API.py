import os
from typing import List

from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import FileResponse
from 发票处理.发票下载.打包下载 import 发票下载
from 用户.登陆.登陆令牌 import 验证令牌

下载API = APIRouter()
security = HTTPBearer()


@下载API.post("/DownZIP")
async def 下载ZIP(
        ID列表: List[int],
        请求: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # 获取 token 和 IP
    token = credentials.credentials
    IP = 请求.client.host

    # 验证令牌
    验证 = 验证令牌(token)
    if not 验证:
        return {'code': 401, 'msg': "Token 无效或过期"}

    # 实例化发票下载类
    下载实例 = 发票下载(验证['sub'], IP)

    # 整理文件列表
    文件列表 = 下载实例.文件列表整理(ID列表)

    # 打包文件
    压缩包 = 下载实例.打包器(文件列表)

    # 检查压缩包是否存在并返回
    if os.path.exists(压缩包):
        return FileResponse(压缩包, filename=os.path.basename(压缩包))
    else:
        return {"code": 400, "msg": "文件不存在"}
