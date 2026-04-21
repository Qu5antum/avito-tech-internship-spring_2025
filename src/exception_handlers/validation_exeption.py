from .base_exception import BaseAppException


class ValidationException(BaseAppException):
    """Вызывается при сбое проверки входных данных."""
    def __init__(self, detail: str):
        super().__init__(detail, status_code=400)