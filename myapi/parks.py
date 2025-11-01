from fastapi import APIRouter
import mysql
from myapi.databases.productdatabase import bakeDataForProduct
import os

router = APIRouter()

@router.post('/parks')
async def get_park(park: dict):
    need_number=park.get("need_number")
    offset_number=park.get("start_id")
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    count_sql = "SELECT COUNT(*) as total FROM shoppers"
    cursor.execute(count_sql)
    total_count = cursor.fetchone()['total']
    sql = "SELECT * FROM shoppers LIMIT %s OFFSET %s"
    try:    
        cursor.execute(sql, (need_number, offset_number))
        parks = cursor.fetchall()
        current_loaded = len(parks)
        has_more = (offset_number + current_loaded) < total_count
        for park in parks:
            sql_fruits = "SELECT * FROM fruits WHERE fruit_shopper = %s"
            cursor.execute(sql_fruits, (park['id'],))
            fruits = cursor.fetchall()
            for fruit in fruits:
                sql_type = "SELECT * FROM types WHERE id = %s"
                cursor.execute(sql_type, (fruit['fruit_type'],))
                type_result = cursor.fetchone()
                if type_result:
                    fruit['fruit_type'] = type_result['type_name']
            park['fruits'] = fruits
            park['has_more'] = has_more
        if parks:
            return parks
        else:
            return {"message": "No parks found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)

@router.get('/info/{user_id}')
async def get_park_by_user(user_id: int):
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        print("No connection")
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    try:
        sql = "SELECT have_park FROM users WHERE id = %s"
        cursor.execute(sql, (user_id,))
        park = cursor.fetchone()
        print(park)
        if park:
            sql_park = "SELECT * FROM shoppers WHERE id = %s"
            cursor.execute(sql_park, (park['have_park'],))
            park_info = cursor.fetchone()
            if park_info:
                print(park_info)
                return park_info
        else:
            return {"message": "Park not found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)

@router.post("/fruits")
def bake_product(product_id_json:dict):
    need_number=product_id_json.get("need_number")
    offset_number=product_id_json.get("start_id")
    user_id=product_id_json.get("user_id")
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    sql_park = "SELECT have_park FROM users WHERE id = %s"
    cursor.execute(sql_park, (user_id,))
    park = cursor.fetchone()
    count_sql = "SELECT COUNT(*) as total FROM fruits WHERE fruit_shopper = %s"
    cursor.execute(count_sql, (park['have_park'],))
    total_count = cursor.fetchone()['total']
    if total_count == 0:
        return []
    sql = "SELECT * FROM fruits WHERE fruit_shopper = %s LIMIT %s OFFSET %s"
    try:    
        sql_park = "SELECT have_park FROM users WHERE id = %s"
        cursor.execute(sql_park, (user_id,))
        park = cursor.fetchone()
        print(park)
        cursor.execute(sql, (park["have_park"], need_number, offset_number))
        product = cursor.fetchall()
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

@router.post("/off_fruit")
def bake_off_product(product_id_json:dict):
    fruit_id=product_id_json.get("fruit_id")
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    try:
        sql = "UPDATE fruits SET is_available = 0 WHERE id = %s"
        cursor.execute(sql, (fruit_id,))
        mysql_conn.commit()
        return {"message": "Fruit taken off successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)

@router.post("/on_fruit")
def bake_on_product(product_id_json:dict):
    fruit_id=product_id_json.get("fruit_id")
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    try:
        sql = "UPDATE fruits SET is_available = 1 WHERE id = %s"
        cursor.execute(sql, (fruit_id,))
        mysql_conn.commit()
        return {"message": "Fruit made available successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)
@router.post("/delete_fruit")
def delete_product(product_id_json:dict):   
    fruit_id=product_id_json.get("fruit_id")
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    try:
        sql_img = "SELECT fruit_image, fruit_image2, fruit_image3, fruit_image4, fruit_image5 FROM fruits WHERE id = %s"
        cursor.execute(sql_img, (fruit_id,))
        images = cursor.fetchall()
        for image in images:
            if(image.get("fruit_image2")):
                image_path = os.path.join("myapi/src", image.get("fruit_image2"))
                if os.path.exists(image_path):
                    os.remove(image_path)
            if(image.get("fruit_image")):
                image_path = os.path.join("myapi/src", image.get("fruit_image"))
                if os.path.exists(image_path):
                    os.remove(image_path)
            if(image.get("fruit_image3")):
                image_path = os.path.join("myapi/src", image.get("fruit_image3"))
                if os.path.exists(image_path):
                    os.remove(image_path)
            if(image.get("fruit_image4")):  
                image_path = os.path.join("myapi/src", image.get("fruit_image4"))
                if os.path.exists(image_path):
                    os.remove(image_path)
            if(image.get("fruit_image5")):  
                image_path = os.path.join("myapi/src", image.get("fruit_image5"))
                if os.path.exists(image_path):
                    os.remove(image_path)
        sql = "DELETE FROM fruits WHERE id = %s"
        cursor.execute(sql, (fruit_id,))
        mysql_conn.commit()
        return {"message": "Fruit deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)