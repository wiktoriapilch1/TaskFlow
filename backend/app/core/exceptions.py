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

class JWTException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_403_FORBIDDEN, 
            detail = "Could not validate credentials.",
        )

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "User not found.",
        )

class UserInactiveException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "User inactive.",
        )