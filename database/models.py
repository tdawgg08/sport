from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
class UserCall(Base):
    __tablename__ = 'user_callories'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    food: Mapped[str] = mapped_column(nullable=True)
    callories: Mapped[int] = mapped_column(nullable=True)

class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

class SubCategory(Base):
    __tablename__ = 'sub_categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()     
    calories: Mapped[int]   
    proteins: Mapped[int]  
    fats: Mapped[int]       
    carbs: Mapped[int]     
    sub_category_id: Mapped[int] = mapped_column(ForeignKey('sub_categories.id'))