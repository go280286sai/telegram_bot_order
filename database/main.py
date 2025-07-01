from datetime import datetime
from sqlalchemy.ext.asyncio import (AsyncSession,
                                    create_async_engine, async_sessionmaker)
from sqlalchemy.orm import (declarative_base,
                            relationship, Mapped, mapped_column)
from sqlalchemy import (Column, Integer, String, Text,
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
    status: Mapped[int] = Column(Integer, default=1, nullable=False)
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


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, unique=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name


class City(Base):
    __tablename__ = "cities"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, unique=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name


class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, unique=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name


class Delivery(Base):
    __tablename__ = "deliveries"
    id: Mapped[int] = Column(Integer, primary_key=True,
                             index=True, autoincrement=True)
    post_id: Mapped[int] = Column(Integer, ForeignKey("posts.id"))
    city_id: Mapped[int] = Column(Integer, ForeignKey("cities.id"))
    address_id: Mapped[int] = Column(Integer, ForeignKey("addresses.id"))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    post: Mapped[Post] = relationship("Post", backref="deliveries")
    city: Mapped[City] = relationship("City", backref="deliveries")
    address: Mapped[Address] = relationship("Address", backref="deliveries")

    def __init__(self, post_id: int, city_id: int, address_id: int, **kwargs):
        super().__init__(**kwargs)
        self.post_id = post_id
        self.city_id = city_id
        self.address_id = address_id


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = Column(Integer, primary_key=True,
                             index=True, autoincrement=True)
    products: Mapped[str] = Column(Text, nullable=False)
    user_id: Mapped[int] = Column(Integer, ForeignKey(User.id), nullable=False)
    delivery_id: Mapped[int] = Column(Integer,
                                      ForeignKey("deliveries.id"),
                                      nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[int] = Column(Integer, default=0)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    user: Mapped[User] = relationship("User", lazy="joined")
    delivery: Mapped[Delivery] = relationship("Delivery", lazy="joined")

    def __init__(self, products: str, user_id: int,
                 delivery_id: int, total: float, **kwargs):
        super().__init__(**kwargs)
        self.products = products
        self.user_id = user_id
        self.delivery_id = delivery_id
        self.total = total


class Carousel(Base):
    __tablename__ = "carousels"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String, nullable=True)
    image: Mapped[str] = Column(String, nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    def __init__(self, title: str, description: str, image: str, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.image = image
        self.created_at = datetime.utcnow()


class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = Column(Text, nullable=False)
    name: Mapped[str] = Column(String, nullable=False)
    gender: Mapped[int] = Column(Integer, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    def __init__(self, text: str, name: str, gender: int, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.name = name
        self.gender = gender
        self.created_at = datetime.utcnow()


engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False)


async def get_db() -> AsyncSession:
    return async_session_maker()
