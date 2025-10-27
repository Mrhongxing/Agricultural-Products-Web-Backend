from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import httpx
from myapi import login
from myapi import images
from myapi import shopping
from myapi import user
from myapi import changes

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, prefix='/apiForLogin')
app.include_router(images.router, prefix='/apiForImages')
app.include_router(shopping.router, prefix='/apiForShopping')
app.include_router(user.router, prefix='/apiForUser')
app.include_router(changes.router, prefix='/apiForChanges')

@app.get('/')
async def root():
    return {'ok': True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('serve:app', host="127.0.0.1", port=8000, reload=True)