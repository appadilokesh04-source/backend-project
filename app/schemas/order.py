
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    address: str

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_price: float
    payment_status: str
    address: str
    created_at: datetime

    class Config:
        orm_mode = True
