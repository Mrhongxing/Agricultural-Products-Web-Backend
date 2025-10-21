from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
import pymysql
from pymysql import Error
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT 配置
TOKEN_KEY="1234567890wcvff" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# MySQL 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'agricultural_products_db',
    'port': 3306,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 获取数据库连接
def get_db_connection():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None
# 关闭数据库连接
def close_db_connection(connection):
    if connection:
        connection.close()
# 解析令牌函数
def validate_token(token: str):
    try:
        payload = jwt.decode(token, TOKEN_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("id")
        username: str = payload.get("username")
        password_hash: str = payload.get("password_hash")
        email: str = payload.get("email")
        role: str = payload.get("role")
        nickname: str = payload.get("nickname")
        if not all([id, username, password_hash, email, role, nickname]):
            return bakeDataForLogin(
                success=False,
                message="Invalid token payload",
                id=0,
                email="",
                role="",
                nickname="",
                token=None
            ).dict()
        else:
            return bakeDataForLogin(
                success=True,
                message="Token is valid",
                id=id,
                email=email,
                role=role, 
                nickname=nickname,
                token=token
            )
    except JWTError:
        return bakeDataForLogin(
            success=False,
            message="Token validation error",
            id=0,
            email="",
            role="",
            nickname="",
            token=None
        )
    except jwt.ExpiredSignatureError:
        return bakeDataForLogin(
            success=False,
            message="Token has expired",
            id=0,
            email="",
            role="",
            nickname="",
            token=None
        )
# 密码哈希函数
def hash_password(plain_password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')
# 密码验证函数
def verify_password(plain_password, hashed_password):
    try :
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        return False
# 创建访问令牌函数
def create_access_token(data: dict,expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TOKEN_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class bakeDataForLogin(BaseModel):
    success: bool
    message: str
    id: int
    email:str
    role:str
    nickname:str
    token: Optional[str] = None

@app.post("/api/register")
async def register(form_data: dict):
    username = form_data.get("username")
    password = form_data.get("password")
    email = form_data.get("email")
    nickname = '默认昵称'
    connection = get_db_connection()
    if not connection:
        return {"success": False, "message": "Database connection error"}
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username=%s"
            cursor.execute(sql,username)
            existing_user = cursor.fetchone()
            if existing_user:
                return {"success": False, "message": "Username already exists"}
            hashed_password = hash_password(password)
            sql = "INSERT INTO users (username, password_hash, email, nickname, role, is_active) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (username, hashed_password, email, nickname, 3, 1))
            connection.commit()
            return {"success": True, "message": "User registered successfully"}
    finally:
        close_db_connection(connection)


@app.post("/api/login")
async def login(form_data: dict):
    username = form_data.get("username")
    password = form_data.get("password")
    connection = get_db_connection()
    if not connection:
        return bakeDataForLogin(
            success=False,
            message="Database connection error",
            id=0,
            email="",
            role="",
            nickname="",
            token=None
        )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username=%s"
            cursor.execute(sql,username)
            user = cursor.fetchone()
            if not user or not verify_password(password, user['password_hash']):
                return bakeDataForLogin(
                    success=False,
                    message="Incorrect username or password",
                    id=0,
                    email="",
                    role="",
                    nickname="",
                    token=None
                )
            elif user['is_active'] == 0:
                return bakeDataForLogin(
                    success=False,
                    message="User account is inactive",
                    id=0,
                    email="",
                    role="",
                    nickname="",
                    token=None
                )
            elif verify_password(password, user['password_hash']):
                if(user['role']) ==1:
                    user['role'] = 'admin'
                elif(user['role'])==2:
                    user['role'] = 'shopper'
                else:
                    user['role'] = 'user'
                tokendata={
                    'id':user['id'],
                    'username':username,
                    'password_hash':user['password_hash'],
                    'email':user['email'],
                    'role':user['role'],
                    'nickname':user['nickname'],
                }
            token = create_access_token(data=tokendata)
            return bakeDataForLogin(
                success=True,
                message="Login successful",
                id=user['id'],
                email=user['email'],
                role=user['role'],
                nickname=user['nickname'],
                token=token
            )
    finally:
        close_db_connection(connection)

@app.post("/api/validate-token")
async def validate_token_endpoint(token_data: dict):
    token = token_data.get("token")
    result = validate_token(token)
    if result is False:
        return bakeDataForLogin(
            success=False,
            message="Token validation failed",
            id=0,
            email="",
            role="",
            nickname="",
            token=None
        )
    else:
        return result
if __name__ == "__main__":
    import uvicorn
    uvicorn.run('serve:app', host="127.0.0.1", port=8000, reload=True)