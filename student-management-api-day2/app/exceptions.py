from fastapi import HTTPException, status

class BaseAppException(HTTPException):
    code: str
    
    def __init__(self, status_code: int, message: str, code: str):
        super().__init__(status_code=status_code, detail=message)
        self.code = code

class DuplicateRegistrationException(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status_code.HTTP_409_CONFLICT,
            message="An account with this email already exists.",
            code="DUPLICATE_REGISTRATION"
        )

class InvalidCredentialsException(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status_code.HTTP_401_UNAUTHORIZED,
            message="Incorrect email or password.",
            code="INVALID_CREDENTIALS"
        )

class TokenExpiredException(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status_code.HTTP_401_UNAUTHORIZED,
            message="Authentication token has expired.",
            code="TOKEN_EXPIRED"
        )

class InvalidTokenException(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status_code.HTTP_401_UNAUTHORIZED,
            message="Could not validate credentials.",
            code="INVALID_TOKEN"
        )

class PermissionDeniedException(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status_code.HTTP_403_FORBIDDEN,
            message="You do not have permission to access this resource.",
            code="PERMISSION_DENIED"
        )