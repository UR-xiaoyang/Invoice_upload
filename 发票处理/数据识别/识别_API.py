from fastapi import Request, Depends, HTTPException, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from 发票处理.数据识别.识别表单 import 表单
from 用户.登陆.登陆令牌 import 验证令牌

from 发票处理.数据识别.发票处理 import 发票处理

识别路由 = APIRouter()
security = HTTPBearer()


@识别路由.post("/Identify_server")
async def ocr_api(表单: 表单, 请求: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    # 提取token
    token = credentials.credentials
    IP = 请求.client.host
    # 验证令牌
    验证 = 验证令牌(token)
    if not 验证:
        raise HTTPException(status_code=401, detail="Token 无效或过期")
    else:
        # 处理发票
        try:
            发票处理实例 = 发票处理(IP, 验证['sub'])
            数据 = 发票处理实例.发票文件处理(表单.发票ID, 表单.OCR)
            发票处理实例.发票数据存入数据库(数据, 表单.发票ID)
            # 返回成功响应到前端
            return {"status": "success", "message": "OCR处理成功", "发票ID": 表单.发票ID}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"发票处理失败: {str(e)}")


