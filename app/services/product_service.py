
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.models.product import Product

def create_product(db: Session, **data):
    p = Product(**data)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: Session, product_id: int, **data):
    p = get_product(db, product_id)
    if not p:
        return None
    for k,v in data.items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

def delete_product(db: Session, product_id: int):
    p = get_product(db, product_id)
    if not p:
        return False
    db.delete(p)
    db.commit()
    return True

def list_products(db: Session, filters: dict, page:int=1, limit:int=10, sort: str=None):
    q = db.query(Product)
    # filters
    if filters.get('price_min') is not None:
        q = q.filter(Product.price >= filters['price_min'])
    if filters.get('price_max') is not None:
        q = q.filter(Product.price <= filters['price_max'])
    if filters.get('metal') is not None:
        q = q.filter(Product.metal_type == filters['metal'])
    if filters.get('polish') is not None:
        q = q.filter(Product.polish_type == filters['polish'])
    # sorting
    if sort == 'latest':
        q = q.order_by(desc(Product.created_at))
    elif sort == 'price_low':
        q = q.order_by(asc(Product.price))
    elif sort == 'price_high':
        q = q.order_by(desc(Product.price))
    elif sort == 'rating':
        q = q.order_by(desc(Product.rating))
    # pagination
    total = q.count()
    items = q.offset((page-1)*limit).limit(limit).all()
    return {'total': total, 'items': items}
