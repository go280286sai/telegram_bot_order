import datetime

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, BOOLEAN, Float, ForeignKey

DATABASE_URL = "sqlite+aiosqlite:///./data.db"

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    status = Column(BOOLEAN, default=True)
    comments = Column(String, nullable=True, default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    description = Column(String)
    amount = Column(Integer, default=None)
    service = Column(BOOLEAN, default=False)
    price = Column(Float, default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    delivery_id = Column(Integer, ForeignKey("deliveries.id"), nullable=False)
    total = Column(Float, default=None)
    status = Column(BOOLEAN, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    product = relationship("Product", lazy="joined")
    user = relationship("User", lazy="joined")
    delivery = relationship("Delivery", lazy="joined")

class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    city = Column(String, unique=True)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    return async_session_maker()
