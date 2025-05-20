from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass 

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    fullname: Mapped[str] = mapped_column

    addresses: Mapped["Address"} = relationship(back_populates="user")

    def __repr__(self):
        return f'User(name={self.name!r}, fullname={self.fullname!r})'

class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")

jack = User(name='jack', fullname='Jack Reacher')


jack.addresses[
    
            Address(email_address='jack@gmail.com'),
            Address(email_address='j25@yahoo.com'),
            Address(email_address='jack@hotmail.com'),
            ]
