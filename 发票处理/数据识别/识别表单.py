from pydantic import BaseModel

class 表单(BaseModel):
    发票ID: int
    OCR: bool = False