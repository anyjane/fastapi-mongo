from fastapi import FastAPI, Depends,Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import HTMLResponse
from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from routes.admin import router as AdminRouter
from routes.student import router as StudentRouter
from routes.dealing import router as DealingRouter
from routes.history import router as HistoryRouter

app = FastAPI()

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await initiate_database()


# @app.get("/", tags=["Root"])
# async def read_root():
#     return {"message": "Welcome to this fantastic app."}


app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
app.include_router(StudentRouter,tags=["Students"],prefix="/student")
app.include_router(DealingRouter,tags=["Dealings"],prefix="/api/dealing")
app.include_router(HistoryRouter,tags=["History"],prefix="/api/history")
app.mount("/main", StaticFiles(directory="static", html=True), name="/")

# 静态文件代理
class RedirectToIndexMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 排除静态文件
        if not request.url.path.endswith((".js", ".css", ".png", ".ico")):
            # 只拦截指定前缀
            if request.url.path.startswith("/admin/") or request.url.path == "/admin":
                return HTMLResponse(content=request.app.index_html, status_code=200)
        response = await call_next(request)
        return response
# 读取index.html
with open("static/index.html", encoding='utf-8') as f:
    app.index_html = f.read()
# 添加中间件
app.add_middleware(RedirectToIndexMiddleware)

# 自定义JS文件的MIME类型为application/javascript
@app.middleware("http")
async def override_static_file_mimetype(request, call_next):
    response = await call_next(request)
    if request.url.path.endswith((".js")):
        response.headers["content-type"] = "application/javascript"
    return response
# 添加中间件
app.add_middleware(RedirectToIndexMiddleware)