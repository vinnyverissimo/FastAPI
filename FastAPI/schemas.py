from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    email: str
    username: str
    hashed_password: str
    admin: Optional[bool]
    active: Optional[bool]

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    product_name: str
    quantity: int

    class Config:
        from_attributes = True


class loginSchema(BaseModel):
    email: str
    hashed_password: str

    class Config:
        from_attributes = True


class OrderItensSchema(BaseModel):
    flavor: str
    size: str
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True
