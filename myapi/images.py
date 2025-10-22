from fastapi import APIRouter
import os
from fastapi.responses import FileResponse
from fastapi import HTTPException

router = APIRouter()

@router.get("/image/{image_name}")
async def get_image(image_name: str):
    filepath = os.path.join("myapi", "src", image_name)
    if os.path.exists(filepath) and filepath.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) :
        return FileResponse(filepath)
    else:
        # 修正3：添加明确的错误处理
        raise HTTPException(status_code=404, detail="Image not found or invalid format")