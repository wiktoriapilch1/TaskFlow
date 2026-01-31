from fastapi import HTTPException, status

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_409_CONFLICT, 
            detail = "User with this email already exists.",
        )

class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Incorrect email or password.", 
            headers = {"WWW-Authenticate": "Bearer"}
        )

class InternalServerError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail = "Critical internal server error. Try again later.",
        )