from .base_exception import BaseAppException


class ReceptionStatusException(BaseAppException):
    def __init__(self, message, status_code = 400):
        super().__init__(message, status_code)