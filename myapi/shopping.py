from fastapi import APIRouter,File, UploadFile, Form,Header
from myapi.databases.productdatabase import bakeDataForProduct
from myapi.login import validate_token
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
    count_sql = "SELECT COUNT(*) as total FROM fruits WHERE is_available = 1"
    cursor.execute(count_sql)
    total_count = cursor.fetchone()['total']
    sql = "SELECT * FROM fruits WHERE is_available = 1 LIMIT %s OFFSET %s"
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

@router.post("/create_park")
async def add_fruit_simple(name:str=Form(...), desc:str=Form(...), location:str=Form(...), phone:str=Form(...), email:str=Form(...), images: List[UploadFile] = File(...), owner_id:str=Form(...), authorization: str = Header(None)):
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    if not authorization:
        return {"success": False, "message": "Unauthorized"}
    token = authorization.split(" ")[1]
    print("Token received:", token)
    userInfo = validate_token(token)
    if not userInfo or userInfo.role != "shopper":
        print(userInfo.username)
        print(userInfo.role)
        return {"success": False, "message": "Unauthorized"}
    if not images:
        return {"success": False, "message": "No image uploaded"}
    print("Received image:", images[0].filename, images[0].content_type)
    try:
        for  i,image in enumerate(images):
            file_extension = get_file_extension(image.filename, image.content_type)
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            upload_path = os.path.join("myapi/src", unique_filename)
            with open(upload_path, "wb") as buffer:
                buffer.write(await image.read())
            if i==0:
                fruit_image=unique_filename
        allow_fields=["shopper_name", "shopper_introduce", "shopper_adress", "shopper_img", "shopper_telephone","shopper_email"]
        park_data = {
            "shopper_name": name,
            "shopper_introduce": desc,
            "shopper_adress": location,
            "shopper_img": fruit_image,
            "shopper_telephone": phone,
            "shopper_email": email
        }
        sql = "INSERT INTO shoppers (shopper_name, shopper_introduction, shopper_address, shopper_img, shopper_telephone, shopper_email) VALUES (%s, %s, %s, %s, %s, %s)"
        params = [park_data[field] for field in allow_fields]
        print("Executing SQL:", sql, params)
        cursor.execute(sql, tuple(params))
        sql_for_owner = "UPDATE users SET have_park = %s WHERE id = %s"
        a=cursor.lastrowid
        cursor.execute(sql_for_owner, (a, owner_id))
        mysql_conn.commit()
        print("Park added successfully.",a)
        return {"success": True, "park_id": a}
    except Exception as e:
        print("Failed to add park:", str(e))
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)

@router.post("/add1")
async def add_fruit_simple(name:str=Form(...), desc:str=Form(...), price:str=Form(...), type:str=Form(...), images: List[UploadFile] = File(...),authorization: str = Header(None)):
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    if not authorization:
        return {"success": False, "message": "Unauthorized"}
    token = authorization.split(" ")[1]
    print("Token received:", token)
    userInfo = validate_token(token)
    if not userInfo or userInfo.role != "shopper":
        print(userInfo.role)
        return {"success": False, "message": "Unauthorized"}
    sql_for_shopper = "SELECT have_park FROM users WHERE id = %s"
    cursor.execute(sql_for_shopper, (userInfo.id,))
    shopper_info = cursor.fetchone()
    fruit_shopper = shopper_info.get('have_park')
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
                fruit_image=unique_filename
            elif i==1:
                fruit_image2=unique_filename
            elif i==2:
                fruit_image3=unique_filename
            elif i==3:
                fruit_image4=unique_filename
            elif i==4:
                fruit_image5=unique_filename
        allow_fields=["fruit_name", "fruit_introduce", "price", "fruit_image", "is_available", "fruit_type", 
                      "fruit_image2", "fruit_image3", "fruit_image4", "fruit_image5", "fruit_shopper"]
        price_ = float(price)
        cursor.execute(f"SELECT * FROM types WHERE type_name = %s", (type,))
        type_ = cursor.fetchone()["id"]
        fruit_data = {
            "fruit_name": name,
            "fruit_introduce": desc,
            "price": price_,
            "fruit_image": fruit_image,
            "is_available": 1,
            "fruit_type": type_,
            "fruit_image": fruit_image,
            "fruit_image2": fruit_image2 if 'fruit_image2' in locals() else None,
            "fruit_image3": fruit_image3 if 'fruit_image3' in locals() else None,
            "fruit_image4": fruit_image4 if 'fruit_image4' in locals() else None,
            "fruit_image5": fruit_image5 if 'fruit_image5' in locals() else None,
            "fruit_shopper": fruit_shopper
        }
        set_fields = []
        params = []
        for field in allow_fields:
            if field in fruit_data and fruit_data[field] is not None:
                set_fields.append(f"{field}")
                params.append(fruit_data[field])
        sql = "INSERT INTO fruits (" + ", ".join(set_fields) + ") VALUES (" + ", ".join(["%s"] * len(params)) + ")"
        print("Executing SQL:", sql, params)
        cursor.execute(sql, tuple(params))
        mysql_conn.commit()
        print("Fruit added successfully.")
        return {"success": True}
    except Exception as e:
        print("Failed to add fruit:", str(e))
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)

@router.get("/fruit_types")
async def get_fruit_types():
    mysql_conn = mysql.get_db_connection()
    if not mysql_conn:
        return {"success": False, "message": "Database connection error"}
    cursor = mysql_conn.cursor()
    try:
        a=[]
        cursor.execute("SELECT * FROM types")
        types = cursor.fetchall()
        for t in types:
            a.append(t['type_name'])
        return a
    except Exception as e:
        print("Failed to retrieve fruit types:", str(e))
        return {"error": str(e)}
    finally:
        mysql.close_db_connection(mysql_conn, cursor)