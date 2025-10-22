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
def close_db_connection(connection):
    if connection:
        connection.close()