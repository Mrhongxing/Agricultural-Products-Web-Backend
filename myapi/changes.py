from fastapi import APIRouter
import mysql
from myapi.login import hash_password
router = APIRouter()

@router.post('/update_password')
async def update_password():

    return {'message': 'Password update endpoint'}
@router.delete('/delete_account')
async def delete_account():

    return {'message': 'Account deletion endpoint'}
@router.post('/change_nickname')
async def change_nickname(changes: dict):
    new_nickname = changes.get("new_nickname")
    id = changes.get("id")
    connection = mysql.get_db_connection()
    if connection is None:
        return {'success': False, 'message': 'Database connection error'}
    try:        
        with connection.cursor() as cursor:
            sql = "UPDATE users SET nickname = %s WHERE id = %s"
            cursor.execute(sql, (new_nickname, id))
        connection.commit()
    except Exception as e:
        return {'success': False, 'message': f'Error updating nickname: {e}'}
    finally:
        mysql.close_db_connection(connection)
    return {'success': True, 'message': 'Nickname changed successfully'}
@router.post('/change_username')
async def change_username(changes: dict):
    new_username = changes.get("new_username")
    id = changes.get("id")
    connection = mysql.get_db_connection()
    if connection is None:
        return {'success': False, 'message': 'Database connection error'}
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE users SET username = %s WHERE id = %s"
            cursor.execute(sql, (new_username, id))
        connection.commit()
    except Exception as e:
        return {'success': False, 'message': f'Error updating username: {e},{new_username}'}
    finally:
        mysql.close_db_connection(connection)
    return {'success': True, 'message': 'Username changed successfully'}
@router.post('/change_email')
async def change_email(changes: dict):
    new_email = changes.get("new_email")
    id = changes.get("id")
    connection = mysql.get_db_connection()
    if connection is None:
        return {'success': False, 'message': 'Database connection error'}
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE users SET email = %s WHERE id = %s"
            cursor.execute(sql, (new_email, id))
        connection.commit()
    except Exception as e:
        return {'success': False, 'message': f'Error updating email: {e}'}
    finally:
        mysql.close_db_connection(connection)

    return {'success': True, 'message': 'Email changed successfully'}
@router.post('/change_password')
async def change_password(changes: dict):
    new_password = changes.get("new_password")
    id = changes.get("id")
    connection = mysql.get_db_connection()
    if connection is None:
        return {'success': False, 'message': 'Database connection error'}
    try:
        password=hash_password(new_password)
        with connection.cursor() as cursor:
            sql = "UPDATE users SET password_hash = %s WHERE id = %s"
            cursor.execute(sql, (password, id))
        connection.commit()
    except Exception as e:
        return {'success': False, 'message': f'Error updating password: {e}'}
    finally:
        mysql.close_db_connection(connection)
    return {'success': True, 'message': 'Password changed successfully'}