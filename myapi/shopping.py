from fastapi import APIRouter
from myapi.databases.productdatabase import bakeDataForProduct
import mysql
    
router = APIRouter()

@router.post("/shopping")
def bake_product(product_id_json:dict):
    need_number=product_id_json.get("need_number")
    offset_number=product_id_json.get("start_id")
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    count_sql = "SELECT COUNT(*) as total FROM fruits"
    cursor.execute(count_sql)
    total_count = cursor.fetchone()['total']
    sql = "SELECT * FROM fruits  LIMIT %s OFFSET %s"
    try:    
        cursor.execute(sql, (need_number, offset_number))
        product = cursor.fetchall()
        print(product)
        if product:
            current_loaded = len(product)
            has_more = (offset_number + current_loaded) < total_count
            formatted = []
            for row in product:
                formatted.append({
                    "id": row.get("id"),
                    "fruit_name": row.get("fruit_name"),
                    "fruit_introduce": row.get("fruit_introduce"),
                    "price": row.get("price"),
                    "fruit_image": row.get("fruit_image"),
                    "is_available": row.get("is_available"),
                    "fruit_type": row.get("fruit_type"),
                    "fruit_image2": row.get("fruit_image2"),
                    "fruit_image3": row.get("fruit_image3"),
                    "fruit_image4": row.get("fruit_image4"),
                    "fruit_image5": row.get("fruit_image5"),
                    "fruit_shopper": row.get("fruit_shopper"),
                    "has_more": has_more,
                })
            return formatted
        else:
            print('ss')
            return bakeDataForProduct(
                product_id=product['id'],
                product_name='Fale',
                product_introduce=product['product_introduce'],
                product_price=product['price'],
                is_available=product['is_available'],
                product_image=product['product_image']
            )
    except Exception as e:
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)
    
@router.post("/add_to_cart")
async def add_to_cart(item: dict):
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    try:
        shopper_sql="SELECT fruit_shopper,price FROM fruits WHERE id=%s"
        cursor.execute(shopper_sql, (item['fruit_id'],))
        fruit_info = cursor.fetchone()
        shopper = fruit_info.get('fruit_shopper')
        price = fruit_info.get('price')
        sql = "INSERT INTO cart (fruit_id, user_id,price,shopper_id) VALUES (%s, %s,%s,%s)"
        cursor.execute(sql, (item['fruit_id'], item['user_id'], price,shopper))
        mysql_conn.commit()
        print("Item added to cart successfully.")
        return {"success": True}
    except Exception as e:
        print("Failed to add item to cart:", str(e))
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)
        