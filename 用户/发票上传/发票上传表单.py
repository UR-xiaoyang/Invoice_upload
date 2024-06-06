from pydantic import BaseModel


class 发票上传表单(BaseModel):
    # 用户名，token，发票的beas64
    用户名: str
    token: str
    #发票: str