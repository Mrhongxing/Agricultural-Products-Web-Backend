from fastapi import APIRouter
import mysql

router = APIRouter()
@router.post('/product')
async def get_product(product: dict):
    fruit_id=product.get("product_id")
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    sql = "SELECT * FROM fruits WHERE id=%s"
    try:  
        cursor.execute(sql, (fruit_id,))
        product = cursor.fetchone()
        if product:
            return {
                "id": product.get("id"),
                "fruit_name": product.get("fruit_name"),
                "fruit_introduce": product.get("fruit_introduce"),
                "price": product.get("price"),
                "fruit_image": product.get("fruit_image"),
                "is_available": product.get("is_available"),
                "fruit_type": product.get("fruit_type"),
                "fruit_image2": product.get("fruit_image2"),
                "fruit_image3": product.get("fruit_image3"),
                "fruit_image4": product.get("fruit_image4"),
                "fruit_image5": product.get("fruit_image5"),
                "fruit_shopper": product.get("fruit_shopper"),
            }
        else:
            return {"message": "Product not found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)