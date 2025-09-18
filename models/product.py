from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from core.db import Base, engine
from datetime import date


class Product(Base):
    """
    Product model for SQLAlchemy to create table
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    fk_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_expire = Column(Date, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)

    user = relationship("User", back_populates="products")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.date_expire and self.date_expire < date.today():
            raise ValueError("The date cannot be before today!")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, date_expire={self.date_expire})>"


Base.metadata.create_all(bind=engine)
