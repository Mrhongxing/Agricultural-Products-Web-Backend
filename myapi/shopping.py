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
    sql = "SELECT * FROM fruits  LIMIT %s OFFSET %s"
    try:    
        cursor.execute(sql, (need_number, offset_number))
        product = cursor.fetchall()
        print(product)
        if product:
            print(type(product))
            return product
        else:
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
        cursor.close()
        mysql_conn.close()
    