from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from myapi import login
from myapi import images
from myapi import shopping
from myapi import user
from myapi import changes
from myapi import parks
from myapi import admin
from myapi import cart
from myapi import product

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 静态文件服务
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(login.router, prefix='/apiForLogin')
app.include_router(images.router, prefix='/apiForImages')
app.include_router(shopping.router, prefix='/apiForShopping')
app.include_router(user.router, prefix='/apiForUser')
app.include_router(changes.router, prefix='/apiForChanges')
app.include_router(parks.router, prefix='/apiForParks')
app.include_router(admin.router, prefix='/apiForAdmin')
app.include_router(cart.router, prefix='/apiForCart')
app.include_router(product.router, prefix='/apiForProduct')

@app.get('/')
async def root():
    return {'ok': True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('serve:app', host="127.0.0.1", port=8000, reload=True)