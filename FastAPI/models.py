from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship

db = create_engine("sqlite:///./database.db")

Base = declarative_base()


# Define your models here, for example:
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True,
                autoincrement=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    # True for active, False for inactive
    active = Column(Boolean, default=True)
    # True for admin, False for regular user
    admin = Column(Boolean, default=False)

    def __init__(self, username: str, email: str, hashed_password: str, active: bool = True, admin: bool = False):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.active = active
        self.admin = admin


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, nullable=False, primary_key=True,
                autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # e.g., pending, completed, cancelled
    status = Column(String, nullable=False, default="pending")
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float)
    Itens = relationship("Itens", cascade="all, delete")

    def __init__(self, user_id: int, product_name: str, quantity: int, total_price: float = 0.0, status: str = "pending"):
        self.user_id = user_id
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = total_price
        self.status = status

    def sumPrice(self):
        self.quantity = len(self.Itens)
        self.total_price = sum(
            item.quantity * item.unit_price for item in self.Itens)


class Itens(Base):
    __tablename__ = "itens"
    id = Column(Integer, nullable=False, primary_key=True,
                autoincrement=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    flavor = Column(String, nullable=False)
    size = Column(String, nullable=False)  # e.g., small, medium, large
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    def __init__(self, order_id: int, flavor: str, size: str, quantity: int, unit_price: float):
        self.order_id = order_id
        self.flavor = flavor
        self.size = size
        self.quantity = quantity
        self.unit_price = unit_price
