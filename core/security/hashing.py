from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    hash_password

    This function provides a hashing for your password.

    parameters:
    - password: the password given by user.

    return:
    - password hashed
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    verify_password

    Function to verify password with hashed password returning True if it's equals or False if is not equals.

    parameters:
    - plain_password (str): the password given by user.
    - hashed_password (str): the password hashed.

    return:
    - True or False
    """
    return pwd_context.verify(plain_password, hashed_password)
