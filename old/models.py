from sqlalchemy import Table, Column, Integer, String, Float, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db import metadata

users = Table('users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(100), unique=True, nullable=False),
    Column('password_hash', String(255), nullable=False),
    Column('role', String(50), default='customer'),
    Column('points', Integer, default=0),
    Column('points_use_limit', Integer, default=100),
    Column('created_at', DateTime, server_default=func.now())
)

products = Table('products', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(200), nullable=False),
    Column('desc', Text),
    Column('price', Float, nullable=False),
    Column('stock', Integer, default=0),
    Column('farm_id', Integer, nullable=True),
    Column('created_at', DateTime, server_default=func.now())
)

orders = Table('orders', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('total', Float, nullable=False),
    Column('used_points', Integer, default=0),
    Column('created_at', DateTime, server_default=func.now())
)

order_items = Table('order_items', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('qty', Integer, default=1),
    Column('price', Float, nullable=False)
)

farms = Table('farms', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(200), nullable=False),
    Column('location', String(255)),
    Column('desc', Text)
)
