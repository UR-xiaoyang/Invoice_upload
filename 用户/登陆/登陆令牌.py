from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

# 定义令牌模型
class 令牌Model(BaseModel):
    访问令牌: str
    令牌类型: str
    过期时间: int

# 生成令牌的函数
def 生成访问令牌(data: dict):
    # 设置令牌过期时间
    过期时间 = datetime.utcnow() + timedelta(minutes=30)
    data.update({"exp": 过期时间})
    编码JWT = jwt.encode(data, "your_secret_key", algorithm="HS256")
    return 编码JWT

# 验证令牌的函数
def 验证令牌(token: str):
    try:
        载荷 = jwt.decode(token, "your_secret_key", algorithms=["HS256"], options={"verify_signature": True})
        return 载荷
    except jwt.exceptions.InvalidTokenError:
        return None
