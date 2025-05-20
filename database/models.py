import datetime
from sqlalchemy import VARCHAR, ForeignKey, BigInteger, TIMESTAMP, Column, String, Integer, Float, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from database.database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger,unique=True)
    first_username: Mapped[str] = mapped_column()
    last_username: Mapped[str] = mapped_column()
    first_answer: Mapped[int] = mapped_column()
    second_answer: Mapped[int] = mapped_column()
    third_answer: Mapped[int] = mapped_column()
    fourth_answer: Mapped[int] = mapped_column()
    fifth_answer: Mapped[int] = mapped_column()
    sixth_answer: Mapped[int] = mapped_column()
    seventh_answer: Mapped[int] = mapped_column()
# class UserCall(Base):
#     __tablename__ = 'user_callories'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
#     food: Mapped[str] = mapped_column(nullable=True)
#     callories: Mapped[int] = mapped_column(nullable=True)

# class Category(Base):
#     __tablename__ = 'categories'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(unique=True)
#     subcategories = relationship("SubCategory", back_populates="category")

# class SubCategory(Base):
#     __tablename__ = 'sub_categories'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))  # Ссылка на id вместо name
#     name: Mapped[str] = mapped_column()
    
#     category = relationship("Category", back_populates="subcategories")
#     products = relationship("Product", back_populates="subcategory")

# class Product(Base):
#     __tablename__ = 'product'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column()
#     calories: Mapped[int]
#     proteins: Mapped[int]
#     fats: Mapped[int]
#     carbs: Mapped[int]
#     sub_category_id: Mapped[int] = mapped_column(ForeignKey('sub_categories.id'))
#     subcategory = relationship("SubCategory", back_populates="products")

class UserTodo(Base):
    __tablename__ = 'users_todo'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        unique=True
    )
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    username = Column(String(50), nullable=True)
    tasks: Mapped[list["Tasks"]] = relationship(back_populates="owner")

class Users(Base):
    __tablename__ = 'users_calories'

    user_id = Column(Integer, primary_key=True, unique=True, nullable=False)

class Tasks(Base):
    __tablename__ = 'tasks'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    is_completed: Mapped[bool] = mapped_column(default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users_todo.user_id", ondelete="CASCADE")
    )
    owner: Mapped["UserTodo"] = relationship(back_populates="tasks")


class Consumption(Base):
    __tablename__ = 'consumption'

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    day = Column(DateTime, nullable=False, default=func.current_timestamp())
    meal_name = Column(VARCHAR(100), nullable=False)
    product_list = Column(Text, nullable=False)
    weight = Column(Integer, nullable=False)
    calories_result = Column(Integer, nullable=False)
    proteins_result = Column(Integer, nullable=False)
    fats_result = Column(Integer, nullable=False)
    carbohydrates_result = Column(Integer, nullable=False)

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    product_name = Column(VARCHAR(255), nullable=False)
    calories = Column(Float, nullable=False)
    proteins = Column(Float, nullable=False)
    fats = Column(Float, nullable=False)
    carbohydrates = Column(Float, nullable=False)    