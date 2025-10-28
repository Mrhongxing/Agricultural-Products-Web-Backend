import pymysql
from pymysql import Error
# MySQL 数据库配置
DB_CONFIG = {
    'host': '8.148.203.93',
    'user': 'root',
    'password': '12345Wcvff',
    'database': 'web_database',
    'port': 13306,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
    
# 获取数据库连接
def get_db_connection():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None
# 关闭数据库连接
def close_db_connection(connection, cursor=None):
    try:
        if cursor:
            cursor.close()
            print("Cursor closed successfully")
    except Exception as e:
        print(f"Error closing cursor: {e}")
    
    try:
        if connection and connection.open:
            connection.close()
            print("Connection closed successfully")
        elif connection:
            print("Connection was already closed")
        else:
            print("Connection was None")
    except Exception as e:
        print(f"Error closing connection: {e}")