from fastapi import APIRouter
import mysql

router = APIRouter()
@router.post('/cart')
async def get_cart(cart: dict):
    need_number=cart.get("need_number")
    offset_number=cart.get("start_id")
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    count_sql = "SELECT COUNT(*) as total FROM cart WHERE user_id=%s"
    cursor.execute(count_sql, (cart['user_id'],))
    total_count = cursor.fetchone()['total']
    sql = "SELECT * FROM cart WHERE user_id=%s LIMIT %s OFFSET %s"
    try:    
        cursor.execute(sql, (cart['user_id'], need_number, offset_number))
        carts = cursor.fetchall()
        current_loaded = len(carts)
        has_more = (offset_number + current_loaded) < total_count
        for cart in carts:
            cart['has_more'] = has_more
            fruit_id=cart['fruit_id']
            fruit_sql="SELECT fruit_name,fruit_introduce,fruit_image,price FROM fruits WHERE id=%s"
            cursor.execute(fruit_sql, (fruit_id,))
            fruit_info = cursor.fetchone()
            cart['fruit_info'] = fruit_info
        if carts:
            return carts
        else:
            return []
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        mysql_conn.close()

@router.post("/remove_from_cart")
async def remove_from_cart(item: dict):
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    print(item  )
    try:
        print("Removing item from cart")
        delete_sql = "DELETE FROM cart WHERE user_id=%s AND fruit_id=%s"
        cursor.execute(delete_sql, (item['user_id'], item['product_id']))
        mysql_conn.commit()
        return {"success": True, "message": "Item removed from cart"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        mysql_conn.close()