from fastapi import APIRouter, UploadFile, Form, File, Request
from 用户.发票.发票上传.发票上传 import 存储发票
from 用户.登陆.登陆令牌 import 验证令牌

发票上传路由 = APIRouter()

@发票上传路由.post("/上传")
async def 发票上传API(
    请求: Request,
    token: str = Form(...),
    用户名: str = Form(...),  # 根据发票上传表单的其他字段添加更多参数
    文件上传: UploadFile = File(...)
):

    验证结果 = 验证令牌(token)
    if 验证结果:
        # 获取IP
        IP = 请求.client.host
        检测上传 = 存储发票(文件上传, 用户名, IP)
        if 检测上传:
            return {"code": 200, "msg": "上传成功"}
        else:
            return {"code": 400, "msg": "上传失败"}
    else:
        return {"code": 400, "msg": "登陆过期"}
