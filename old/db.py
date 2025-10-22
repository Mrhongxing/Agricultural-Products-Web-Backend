from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import pymysql

pymysql.install_as_MySQLdb()  # 注册 PyMySQL 为 MySQLdb，避免 ModuleNotFoundError

# 使用环境变量或默认连接串
DATABASE_URL = 'mysql+aiomysql://root:password@127.0.0.1:3306/agri_db'

engine = create_engine(DATABASE_URL.replace('+aiomysql', ''), echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
