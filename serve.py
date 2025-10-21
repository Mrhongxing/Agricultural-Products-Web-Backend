from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import httpx
import os
from myapi import login

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, prefix='/apiForLogin')

@app.get('/')
async def root():
    return {'ok': True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('serve:app', host="127.0.0.1", port=8000, reload=True)