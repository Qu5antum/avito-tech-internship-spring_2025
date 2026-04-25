from .base_exception import BaseAppException


class ProductNotFoundException(BaseAppException):
    def __init__(self, message, status_code = 404):
        super().__init__(message, status_code)