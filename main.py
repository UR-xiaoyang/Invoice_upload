from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from 用户.发票.发票上传.发票上传API import 发票上传路由
from 用户.发票.发票查询.发票查询API import 发票查询路由器
from 用户.注册.注册API import 注册路由
from 用户.登陆.登陆API import 登陆路由
from 发票处理.OCR.OCR_API import OCR路由

app = FastAPI()

# 设置允许所有来源的CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含 API 路由
app.include_router(注册路由, prefix="/user")
app.include_router(登陆路由, prefix="/user")
app.include_router(发票上传路由, prefix="/user")  # 修改前缀以避免冲突
app.include_router(发票查询路由器, prefix="/user")  # 修改前缀以避免冲突
app.include_router(OCR路由, prefix="/ocr")

# 添加对 OPTIONS 请求的处理
@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    response = JSONResponse({"message": "CORS preflight"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# 启动 FastAPI 应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
