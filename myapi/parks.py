from fastapi import APIRouter
import mysql

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
            print(parks)
            return parks
        else:
            return {"message": "No parks found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        mysql_conn.close()