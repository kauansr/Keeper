from fastapi import Request
from core.security.jwt import decode_access_token


async def add_user_to_request_state(request: Request, call_next):
    """
    Middleware to get the header, decode and add the user data to request.state.user

    parameters:
    - request (Request): to get header and add to state.user
    - call_next: call the next middleware

    return:
    - next middleware if success
    - nothing if not success
    """
    token = request.headers.get("Authorization")

    if token:
        try:
            token = token.split(" ")[1]

            user_data = decode_access_token(token)
            request.state.user = user_data
        except Exception:

            request.state.user = None
    else:

        request.state.user = None

    response = await call_next(request)
    return response
