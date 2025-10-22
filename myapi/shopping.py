from fastapi import APIRouter
from myapi.databases.productdatabase import bakeDataForProduct
import mysql
    
router = APIRouter()

@router.post("/shopping")
def bake_product(product_id_json:dict):
    product_id=product_id_json.get("id")
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    sql = "SELECT * FROM products WHERE id = %s"
    try:    
        cursor.execute(sql, product_id)
        product = cursor.fetchone()
        if product:
            return bakeDataForProduct(
                product_id=product['id'],
                product_name=product['name'],
                product_introduce=product['product_introduce'],
                product_price=product['price'],
                is_available=product['is_available'],
                product_image=product['product_image']
            ).dict()
        else:
            return bakeDataForProduct(
                product_id=product['id'],
                product_name=product['name'],
                product_introduce=product['product_introduce'],
                product_price=product['price'],
                is_available=product['is_available'],
                product_image=product['product_image']
            ).dict()
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        mysql_conn.close()
    