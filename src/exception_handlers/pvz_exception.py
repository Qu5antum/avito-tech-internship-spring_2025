from .base_exception import BaseAppException


class PVZNotFountException(BaseAppException):
    def __init__(self, detail, status_code = "404"):
        super().__init__(detail, status_code)
