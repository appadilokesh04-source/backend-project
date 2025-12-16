
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.order import OrderCreate, OrderOut
from app.services.order_service import create_order, get_orders_for_user, get_order
from app.routes.users import get_current_user

router = APIRouter()

@router.post('', response_model=OrderOut)
def create(o: OrderCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    order = create_order(db, current_user.id, [item.dict() for item in o.items], o.address)
    return order

@router.get('')
def list_orders(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_orders_for_user(db, current_user.id)

@router.get('/{id}', response_model=OrderOut)
def get_one(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    order = get_order(db, id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail='Order not found')
    return order
