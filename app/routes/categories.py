
#from fastapi import APIRouter, Depends, HTTPException
#from sqlalchemy.orm import Session
#from app.config.database import get_db
#from app.services.category_service import list_categories, get_category_products
#from app.schemas.category import CategoryOut
#from typing import List

#router = APIRouter()

#@router.get('', response_model=List[CategoryOut])
#def categories(db: Session = Depends(get_db)):
 #   return list_categories(db)

#@router.get('/{id}/products')
#def products_by_category(id: int, db: Session = Depends(get_db)):
#    return get_category_products(db, id)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.post("/", response_model=CategoryOut)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    exists = db.query(Category).filter(Category.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(
        name=payload.name,
        image_url=payload.image_url
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
