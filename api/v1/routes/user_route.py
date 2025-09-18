from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from schemas.user import ProductCreate, UserLogin, UserResponse, ProductUpdate
from services.user_service import UserService
from api.v1.dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from core.security.jwt import create_access_token
from core.security.hashing import verify_password
from models.user import Product

user_route = APIRouter()


def get_user_service(db: Session = Depends(get_db)):
    """
    get the user services

    This function returns all user services from services.
    """
    return UserService(db)


@user_route.get("/user", response_model=list[UserResponse])
async def get_users(user_service: UserService = Depends(get_user_service)):
    """
    List all users.

    This endpoint retrieves a list of all users from the system.

    Parameters:
    - user_service (UserService): Dependency that provides the user service instance used to fetch users.

    Responses:
    - 200 OK: A list of users in the `UserResponse` format.
    - 400 Bad Request: If no users are found, a `400` status is returned with the message "Any Users!".

    Example usage:
    - Request: GET /user
    - Response: List of users or 400 if no users exist.
    """
    users = user_service.list_users()
    if not users:
        HTTPException(status_code=400, detail="Any Users!")
    return users


@user_route.post("/user", response_model=UserResponse)
async def create_user(
    body: ProductCreate, user_service: UserService = Depends(get_user_service)
):
    """
    Create a new user.

    This endpoint creates a new user in the system using the provided data.

    Parameters:
    - body (UserCreate): The request body containing the information for creating a new user.
    - user_service (UserService): Dependency that provides the user service instance to handle user creation.

    Responses:
    - 201 Created: The newly created user in the `UserResponse` format.
    - 400 Bad Request: If the user creation fails due to invalid credentials, a `400` status is returned with the message "Invalid credentials!".

    Example usage:
    - Request: POST /user with user data in the body.
    - Response: Newly created user or 400 if invalid credentials are provided.
    """
    user_created = user_service.create_user(body)
    if not user_created:
        HTTPException(status_code=400, detail="Invalid credentials!")
    return user_created


@user_route.put("/user/update/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: ProductUpdate,
    user_service: UserService = Depends(get_user_service),
):
    """
    Update an existing user.

    This endpoint updates an existing user's data based on the provided user ID and new user data.

    Parameters:
    - user_id (int): The ID of the user to be updated.
    - user_data (UserUpdate): The new data for the user.
    - user_service (UserService): Dependency that provides the user service instance used to update the user.

    Responses:
    - 200 OK: The updated user information in the `UserResponse` format.
    - 400 Bad Request: If the update operation fails, a `400` status is returned with the message "Update error!".

    Example usage:
    - Request: PUT /user/update/{user_id} with updated user data.
    - Response: Updated user or 400 if the update fails.
    """

    update_user = user_service.update_user(user_id, user_data)

    if not update_user:
        HTTPException(status_code=400, detail="Update error!")

    return update_user


@user_route.delete("/user/{id_user}")
async def delete_user(
    id_user: int, user_service: UserService = Depends(get_user_service)
):
    """
    Delete a user by ID.

    This endpoint deletes the user identified by the given user ID.

    Parameters:
    - id_user (int): The ID of the user to be deleted.
    - user_service (UserService): Dependency that provides the user service instance to perform deletion.

    Responses:
    - 200 OK: Returns a success message when the user is deleted.
    - 400 Bad Request: If the user deletion fails, a `400` status is returned with the message "User not deleted!".

    Example usage:
    - Request: DELETE /user/{id_user}
    - Response: Confirmation message or 400 if deletion fails.
    """
    delete_service = user_service.delete_user(id_user)

    if not delete_service:
        HTTPException(status_code=400, detail="User not deleted!")
    return JSONResponse(content={"message": "Deleted successefuly!"}, status_code=200)


@user_route.post("/login")
async def login(
    body: UserLogin,
    user_service: UserService = Depends(get_user_service),
):
    """
    Authenticate a user and generate an access token.

    This endpoint allows a user to log in by verifying their email and password.
    If the credentials are valid, it returns a JWT access token for authentication.

    Parameters:
    - body (UserLogin): The request body containing the user's email and password.
    - user_service (UserService): Dependency that provides the user service instance to fetch user data.

    Responses:
    - 200 OK: Returns an access token and token type in the response body and an Authorization header.
    - 400 Bad Request: If the email does not exist or the password is incorrect, a 400 status with "Invalid credentials!" is returned.

    Example usage:
    - Request: POST /login with JSON body { "email": "user@example.com", "password": "password123" }
    - Response: JSON with access token and bearer token type or 400 if invalid credentials.
    """

    user = user_service.get_user_by_email(body.email)
    if user:
        if verify_password(body.password, user.hashed_password):
            access_token = create_access_token(data={"sub": body.email})
            return JSONResponse(
                content={"access_token": access_token, "token_type": "bearer"},
                headers={"Authorization": f"Bearer {access_token}"},
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid credentials!")
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials!")
