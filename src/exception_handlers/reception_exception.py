from .base_exception import BaseException


class ReceptionStatusException(BaseException):
    def __init__(self, detail, status_code = "400"):
        super().__init__(detail, status_code)