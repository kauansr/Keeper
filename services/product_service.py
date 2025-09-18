from sqlalchemy.orm import Session
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate
from repository.product_repo import ProductRepo
from typing import List, Optional


class ProductService:
    """
    the User services providing functions to connect with the repository
    """

    def __init__(self, db: Session):
        self.product_repo = ProductRepo(db)

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """
        get product by id returning the product

        parameters:
        - product_id (int): the product id

        return:
        - product
        """
        return self.product_repo.get_product_by_id(product_id)

    def get_product_by_name(self, name: str) -> Optional[Product]:
        """
        get the product name
        """

        return self.product_repo.get_product_by_name(name)

    def create_product(self, product_data: ProductCreate) -> Product:

        return self.product_repo.create_product(product_data)

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:

        product = self.get_product_by_id(product_id)

        if product is None:
            return None

        if product_data.name:
            product.name = product_data.name
        if product_data.date_expire:
            product.date_expire = product_data.date_expire
        if product_data.price:
            product.price = product_data.price

        return self.product_repo.update_product(product_id, product)

    def list_product(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.product_repo.list_products(skip, limit)

    def delete_product(self, product_id: int) -> bool:

        return self.product_repo.delete_product(product_id)
