from sqlalchemy.orm import Session
from models.user import Product
from schemas.user import ProductCreate, ProductUpdate
from core.security.hashing import hash_password
from typing import Optional, List


class ProductRepo:
    """
    User repository that provides many functions connecting with database
    """

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[Product]:
        """
        get users by id inside the database returning the user

        parameters:
        - user_id (int): the user id

        return:
        - User
        """
        return self.db.query(Product).filter(Product.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[Product]:
        """
        get user by email inside the database retuning the user

        parameters:
        - email (str): the users email

        return:
        - User
        """
        return self.db.query(Product).filter(Product.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[Product]:
        """
        get user by username inside the database retuning the user

        parameters:
        - username (str): the users username

        return:
        - User
        """
        return self.db.query(Product).filter(Product.name == username).first()

    def create_user(self, user_data: ProductCreate) -> Product:
        """
        Create an account for the user returning the User

        parameters:
        - user_data (UserCreate): the user data to create the account

        return:
        - User
        """
        hashed_pwd = hash_password(user_data.password)
        new_user = Product(
            name=user_data.name, email=user_data.email, hashed_password=hashed_pwd
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def list_users(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        list of all users retuning User

        parameters:
        - skip (int): where start the much accounts you can get
        - limit (int): where end the list

        return:
        - User
        """
        return self.db.query(Product).offset(skip).limit(limit).all()

    def update_user(self, user_id: int, user: Product) -> Optional[Product]:
        """
        update an user in database returning User

        parameters:
        - user_id (int): the user id
        - user (User): the User data

        return:
        - User
        """

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        """
        delete an user in the database returning True

        parameters:
        - user_id (int): the user id

        return:
        - True
        """
        user = self.get_user_by_id(user_id)

        self.db.delete(user)
        self.db.commit()
        return True
