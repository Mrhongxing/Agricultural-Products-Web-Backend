from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from db import SessionLocal
from models import products, orders, order_items, users

router = APIRouter()

@router.get('/')
def list_products():
    db = SessionLocal()
    rows = db.execute(products.select()).fetchall()
    return [dict(r) for r in rows]

@router.post('/')
def create_product(payload: dict):
    db = SessionLocal()
    res = db.execute(products.insert().values(**payload))
    db.commit()
    return {'ok': True, 'id': res.lastrowid}

@router.post('/order')
def create_order(payload: dict):
    # payload: { user_id, items: [{product_id, qty, price}], used_points }
    db = SessionLocal()
    total = sum(i['qty'] * i['price'] for i in payload.get('items', []))
    used = int(payload.get('used_points', 0) or 0)
    res = db.execute(orders.insert().values(user_id=payload['user_id'], total=total, used_points=used))
    order_id = res.lastrowid
    for it in payload.get('items', []):
        db.execute(order_items.insert().values(order_id=order_id, product_id=it['product_id'], qty=it['qty'], price=it['price']))
    # 奖励积分：例如按消费总额的5%返还（活动期间可更改）
    points_awarded = int(total * 0.05)
    db.execute(users.update().where(users.c.id == payload['user_id']).values(points=users.c.points + points_awarded))
    db.commit()
    return {'ok': True, 'order_id': order_id, 'points_awarded': points_awarded}
