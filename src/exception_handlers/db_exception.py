from .base_exception import BaseAppException


class DatabaseException(BaseAppException):
    def __init__(self, detail, status_code = "DB_ERROR"):
        super().__init__(detail, status_code)