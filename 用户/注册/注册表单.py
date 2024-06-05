from pydantic import BaseModel

class 注册表单(BaseModel):
    用户名: str
    密码: str
    邮箱: str
    银行卡号: str
    开户行: str
    真实姓名: str
    部门名称: str