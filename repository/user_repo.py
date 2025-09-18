from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.security.hashing import hash_password
from typing import Optional, List


class UserRepo:
    """
    User repository that provides many functions connecting with database
    """

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        get users by id inside the database returning the user

        parameters:
        - user_id (int): the user id

        return:
        - User
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        get user by email inside the database retuning the user

        parameters:
        - email (str): the users email

        return:
        - User
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        get user by username inside the database retuning the user

        parameters:
        - username (str): the users username

        return:
        - User
        """
        return self.db.query(User).filter(User.name == username).first()

    def create_user(self, user_data: UserCreate) -> User:
        """
        Create an account for the user returning the User

        parameters:
        - user_data (UserCreate): the user data to create the account

        return:
        - User
        """
        hashed_pwd = hash_password(user_data.password)
        new_user = User(
            name=user_data.name, email=user_data.email, hashed_password=hashed_pwd
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        list of all users retuning User

        parameters:
        - skip (int): where start the much accounts you can get
        - limit (int): where end the list

        return:
        - User
        """
        return self.db.query(User).offset(skip).limit(limit).all()

    def update_user(self, user_id: int, user: User) -> Optional[User]:
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
