from pydantic import BaseModel, Field
from datetime import date


class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    fk_user: int
    date_expire: date
    price: float


class ProductResponse(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=50)
    fk_user: int
    date_expire: date
    price: float


class ProductUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    date_expire: date
    price: float
