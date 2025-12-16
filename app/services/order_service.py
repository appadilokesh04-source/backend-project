
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product

def create_order(db: Session, user_id: int, items: list, address: str):
    total = 0.0
    for it in items:
        prod = db.query(Product).filter(Product.id == it['product_id']).first()
        if not prod:
            raise Exception(f'Product {it["product_id"]} not found')
        if prod.stock < it['quantity']:
            raise Exception(f'Insufficient stock for product {prod.id}')
        total += prod.price * it['quantity']
        prod.stock -= it['quantity']
    order = Order(user_id=user_id, total_price=total, address=address, payment_status='pending')
    db.add(order)
    db.commit()
    db.refresh(order)
    for it in items:
        oi = OrderItem(order_id=order.id, product_id=it['product_id'], quantity=it['quantity'], unit_price=db.query(Product).get(it['product_id']).price)
        db.add(oi)
    db.commit()
    return order

def get_orders_for_user(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()
