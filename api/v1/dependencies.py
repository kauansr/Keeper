from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.db import SessionLocal
from core.security.jwt import decode_access_token
from core.security.oauth import oauth2_scheme
from repository.user_repo import ProductRepo
from models.user import Product


def get_db():
    """
    This function manages the database session lifecycle. It creates a session for interaction
    with the database and ensures that the session is closed once the operations are completed.

    Yields:
        db: The database session that can be used to interact with the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Product:
    """
    Retrieves the current user based on the provided OAuth2 token.

    Args:
        token (str): The OAuth2 access token, retrieved from the Authorization header.
        db (Session): The current database session, provided by dependency injection.

    Returns:
        User: The user object corresponding to the email found in the token's payload.

    Raises:
        HTTPException: If the token is invalid, or if the user is not found.
    """
    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user_email = str(payload["sub"])

    userrepo = ProductRepo(db)
    user = userrepo.get_user_by_email(user_email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
