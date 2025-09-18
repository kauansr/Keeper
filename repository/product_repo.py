from sqlalchemy.orm import Session
from models.product import Product
from schemas.user import ProductCreate, ProductUpdate
from core.security.hashing import hash_password
from typing import Optional, List


class ProductRepo:
    """
    Product repository that provides many functions connecting with database
    """

    def __init__(self, db: Session):
        self.db = db

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """
        get products by id inside the database returning the Product

        parameters:
        - product_id (int): the product id

        return:
        - product
        """
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_product_by_name(self, name: str) -> Optional[Product]:
        """
        get product by name inside the database retuning the product

        parameters:
        - name (str): the product name

        return:
        - Product
        """
        return self.db.query(Product).filter(Product.name == name).first()

    def create_product(self, product_data: Product) -> Product:
        """
        Create a product and return the Product

        parameters:
        - product_data (ProductCreate): the product data to create

        return:
        - Product
        """
        new_product = product_data
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def list_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        list of all product retuning Product

        parameters:
        - skip (int): where start the much products you can get
        - limit (int): where end the list

        return:
        - Product
        """
        return self.db.query(Product).offset(skip).limit(limit).all()

    def update_product(self, product_id: int, product: Product) -> Optional[Product]:
        """
        update an Product in database returning Product

        parameters:
        - product_id (int): the Product id
        - product (Product): the Product data

        return:
        - Product
        """
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: int) -> bool:
        """
        delete an product in the database returning True

        parameters:
        - product_id (int): the Product id

        return:
        - True
        """
        product = self.get_product_by_id(product_id)

        self.db.delete(product)
        self.db.commit()
        return True
