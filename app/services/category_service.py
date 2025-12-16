
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.product import Product

def list_categories(db: Session):
    return db.query(Category).all()

def get_category_products(db: Session, category_id: int):
    return db.query(Product).filter(Product.category_id == category_id).all()
