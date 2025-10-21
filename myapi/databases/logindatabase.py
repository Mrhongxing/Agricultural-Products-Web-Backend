from pydantic import BaseModel
from typing import Optional

class bakeDataForLogin(BaseModel):
    success: bool
    message: str
    id: int
    email:str
    role:str
    nickname:str
    token: Optional[str] = None