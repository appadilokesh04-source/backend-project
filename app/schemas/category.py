
#from pydantic import BaseModel
#from typing import Optional, List
#from app.schemas.product import ProductOut

#class CategoryBase(BaseModel):
   # name: str
  #  image_url: str | None = None

#class CategoryOut(CategoryBase):
   # id: int
    #image_url: Optional[str] = None

    #class Config:
      #  orm_mode = True
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    image_url: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True
