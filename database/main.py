from datetime import datetime
from sqlalchemy.ext.asyncio import (AsyncSession,
                                    create_async_engine, async_sessionmaker)
from sqlalchemy.orm import (declarative_base,
                            relationship, Mapped, mapped_column)
from sqlalchemy import (Column, Integer, String,
                        DateTime, Float, ForeignKey)

DATABASE_URL = "sqlite+aiosqlite:///./data.db"

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True,
                             index=True, autoincrement=True)
    username: Mapped[str] = Column(String, unique=True, index=True)
    password: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String, unique=True, nullable=False)
    phone: Mapped[str] = Column(String, unique=True, nullable=True)
    status: Mapped[int] = Column(Integer, default=0, nullable=False)
    comments: Mapped[str] = Column(String, nullable=True, default=None)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = Column(Integer, primary_key=True,
                             index=True, autoincrement=True)
    name: Mapped[str] = Column(String, unique=True)
    description: Mapped[str] = Column(String, nullable=True)
    amount: Mapped[int] = Column(Integer, default=None)
    service: Mapped[int] = Column(Integer, default=0)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    def __init__(self, name: str, description: str,
                 amount: int, price: float, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.amount = amount
        self.price = price


class Delivery(Base):
    __tablename__ = "deliveries"
    id: Mapped[int] = Column(Integer, primary_key=True,
                             index=True, autoincrement=True)
    name: Mapped[str] = Column(String, unique=True)
    city: Mapped[str] = Column(String, unique=True)
    address: Mapped[str] = Column(String)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = Column(Integer, primary_key=True,
                             index=True, autoincrement=True)
    product_id: Mapped[int] = Column(Integer,
                                     ForeignKey(Product.id), nullable=False)
    user_id: Mapped[int] = Column(Integer, ForeignKey(User.id), nullable=False)
    delivery_id: Mapped[int] = Column(Integer,
                                      ForeignKey("deliveries.id"),
                                      nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[int] = Column(Integer, default=0)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    product: Mapped[Product] = relationship("Product", lazy="joined")
    user: Mapped[User] = relationship("User", lazy="joined")
    delivery: Mapped[Delivery] = relationship("Delivery", lazy="joined")

    def __init__(self, product_id: int, user_id: int,
                 delivery_id: int, total: float, **kwargs):
        super().__init__(**kwargs)
        self.product_id = product_id
        self.user_id = user_id
        self.delivery_id = delivery_id
        self.total = total


engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(
                                         engine,
                                         class_=AsyncSession,
                                         expire_on_commit=False)


async def get_db() -> AsyncSession:
    return async_session_maker()
