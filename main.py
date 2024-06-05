from fastapi import FastAPI
from 用户.注册.注册API import 注册路由
from 用户.登陆.登陆API import 登陆路由

# 导入其他 API 路由...

app = FastAPI()

# 包含 API 路由
app.include_router(注册路由, prefix="/用户")
app.include_router(登陆路由, prefix="/用户")
# 包含其他 API 路由...

# 启动 FastAPI 应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
