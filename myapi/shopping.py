from fastapi import APIRouter,File, UploadFile, Form
from myapi.databases.productdatabase import bakeDataForProduct
import mysql
import uuid
import os
from typing import List
    
router = APIRouter()

def get_file_extension(filename: str, content_type: str) -> str:
    """根据文件名或Content-Type获取文件扩展名"""
    if filename and '.' in filename:
        return os.path.splitext(filename)[1]
    
    # 根据MIME类型确定扩展名
    extension_map = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif"
    }
    return extension_map.get(content_type, ".jpg")

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

@router.post("/add")
async def add_fruit(fruit: dict):
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    try:
        sql = """INSERT INTO fruits 
                 (fruit_name, fruit_introduce, price, fruit_image, is_available, fruit_type, 
                  fruit_image2, fruit_image3, fruit_image4, fruit_image5, fruit_shopper) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (
            fruit['fruit_name'], fruit['fruit_introduce'], fruit['price'], fruit['fruit_image'],
            fruit['is_available'], fruit['fruit_type'], fruit['fruit_image2'], fruit['fruit_image3'],
            fruit['fruit_image4'], fruit['fruit_image5'], fruit['fruit_shopper']
        ))
        mysql_conn.commit()
        print("Fruit added successfully.")
        return {"success": True}
    except Exception as e:
        print("Failed to add fruit:", str(e))
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)

@router.post("/add1")
async def add_fruit_simple(name:str=Form(...), desc:str=Form(...), price:str=Form(...), type:str=Form(...), images: List[UploadFile] = File(...)):
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    if not images:
        return {"error": "No image uploaded"}
    print("Received image:", images[0].filename, images[0].content_type)
    try:
        for  i,image in enumerate(images):
            file_extension = get_file_extension(image.filename, image.content_type)
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            upload_path = os.path.join("myapi/src", unique_filename)
            with open(upload_path, "wb") as buffer:
                buffer.write(await image.read())
            if i==0:
                fruit_image=upload_path
            elif i==1:
                fruit_image2=upload_path
            elif i==2:
                fruit_image3=upload_path
            elif i==3:
                fruit_image4=upload_path
            elif i==4:
                fruit_image5=upload_path
    except Exception as e:
        print("Failed to add fruit:", str(e))
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)