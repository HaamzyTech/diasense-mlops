from fastapi import status


class AppError(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class DependencyError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


class ValidationError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
