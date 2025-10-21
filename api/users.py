from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from db import SessionLocal
from models import users

router = APIRouter()

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    points: int

@router.get('/')
def list_users():
    db = SessionLocal()
    rows = db.execute(users.select()).fetchall()
    return [dict(r) for r in rows]

@router.get('/{user_id}')
def get_user(user_id: int):
    db = SessionLocal()
    r = db.execute(users.select().where(users.c.id == user_id)).first()
    if not r: raise HTTPException(404, 'User not found')
    return dict(r)
