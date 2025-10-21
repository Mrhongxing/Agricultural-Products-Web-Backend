from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from db import SessionLocal
from models import users

router = APIRouter()
pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET = 'dev-secret-change'

class LoginIn(BaseModel):
    username: str
    password: str

class RegisterIn(BaseModel):
    username: str
    password: str
    role: str = 'customer'

def create_token(data: dict, expires_minutes: int = 60*24*7):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET, algorithm='HS256')

@router.post('/register')
def register(payload: RegisterIn):
    db = SessionLocal()
    existing = db.execute(users.select().where(users.c.username == payload.username)).first()
    if existing:
        raise HTTPException(400, '用户名已存在')
    hashp = pwd_ctx.hash(payload.password)
    res = db.execute(users.insert().values(username=payload.username, password_hash=hashp, role=payload.role))
    db.commit()
    return {'ok': True}

@router.post('/login')
def login(payload: LoginIn):
    db = SessionLocal()
    row = db.execute(users.select().where(users.c.username == payload.username)).first()
    if not row or not pwd_ctx.verify(payload.password, row.password_hash):
        raise HTTPException(400, '用户名或密码错误')
    token = create_token({'sub': row.username, 'role': row.role, 'user_id': row.id})
    return {'access_token': token, 'token_type': 'bearer'}
