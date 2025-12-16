
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.config.database import get_db
from app.schemas.product import ProductCreate, ProductOut
from app.services.product_service import create_product, get_product, update_product, delete_product, list_products
from app.routes.users import get_current_user
from fastapi import status

router = APIRouter()

@router.get('', response_model=dict)
def list_all(price_min: Optional[float]=Query(None), price_max: Optional[float]=Query(None),
             metal: Optional[str]=Query(None), polish: Optional[str]=Query(None),
             sort: Optional[str]=Query(None), page: int=1, limit: int=10, db: Session = Depends(get_db)):
    filters = {'price_min': price_min, 'price_max': price_max, 'metal': metal, 'polish': polish}
    res = list_products(db, filters, page, limit, sort)
    return {'total': res['total'], 'items': [ProductOut.from_orm(i) for i in res['items']]}

@router.get('/{id}', response_model=ProductOut)
def get_one(id: int, db: Session = Depends(get_db)):
    p = get_product(db, id)
    if not p:
        raise HTTPException(status_code=404, detail='Product not found')
    return p

@router.post('', response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create(p: ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail='Admin only')
    prod = create_product(db, **p.dict())
    return prod

@router.put('/{id}', response_model=ProductOut)
def update(id: int, payload: ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail='Admin only')
    prod = update_product(db, id, **payload.dict())
    if not prod:
        raise HTTPException(status_code=404, detail='Product not found')
    return prod

@router.delete('/{id}', status_code=204)
def remove(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail='Admin only')
    ok = delete_product(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail='Product not found')
    return None
