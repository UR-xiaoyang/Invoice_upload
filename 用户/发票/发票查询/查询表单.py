from pydantic import BaseModel

class 发票查询表单(BaseModel):
    用户: str
    token: str
    页码: int

