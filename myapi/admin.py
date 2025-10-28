from fastapi import APIRouter, Depends
import mysql
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from myapi.login import validate_token

router = APIRouter()
security = HTTPBearer()
@router.post('/admin-management')
def create_admin(need_data: dict, credentials: HTTPAuthorizationCredentials=Depends(security)):
    need_number = need_data.get("need_number")
    offset_number = need_data.get("start_id")
    token = credentials.credentials
    # Here you would normally validate the token
    userInfo = validate_token(token)
    if not userInfo or userInfo.role != "admin":
        return {"success": False, "message": "Unauthorized"}
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    count_sql = "SELECT COUNT(*) as total FROM users"
    try:
        cursor.execute(count_sql)
        total_count = cursor.fetchone()['total']
        sql = "SELECT id, username, email, role, nickname, is_active FROM users LIMIT %s OFFSET %s"
        cursor.execute(sql, (need_number, offset_number))
        users = cursor.fetchall()
        current_loaded = len(users)
        has_more = (offset_number + current_loaded) < total_count
        print(has_more  )
        for user in users:
            user['has_more'] = has_more
        if users:
            return users
        else:
            return {'id': -1,
                    'username': '',
                    'email': '',
                    'role': '',
                    'nickname': '',
                    'is_active': '',
                    'has_more': False
                }
    except Exception as e:
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)