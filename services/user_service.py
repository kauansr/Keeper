from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate
from repository.user_repo import UserRepo
from typing import List, Optional
from core.security.hashing import hash_password


class UserService:
    """
    the User services providing functions to connect with the repository
    """

    def __init__(self, db: Session):
        self.user_repo = UserRepo(db)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        get user by id returning the User

        parameters:
        - user_id (int): the user id

        return:
        - User
        """
        return self.user_repo.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        get the user by email returning the User

        parameters:
        - email (str): the user email

        return:
        - User
        """
        return self.user_repo.get_user_by_email(email)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        get the username
        """

        return self.user_repo.get_user_by_username(username)

    def create_user(self, user_data: UserCreate) -> User:

        existing_user = self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already in use.")

        return self.user_repo.create_user(user_data)

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:

        user = self.get_user_by_id(user_id)

        if user is None:
            return None

        if user_data.name:
            user.name = user_data.name
        if user_data.email:
            user.email = user_data.email
        if user_data.password:

            user.hashed_password = hash_password(user_data.password)

        return self.user_repo.update_user(user_id, user)

    def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.user_repo.list_users(skip, limit)

    def delete_user(self, user_id: int) -> bool:

        return self.user_repo.delete_user(user_id)
