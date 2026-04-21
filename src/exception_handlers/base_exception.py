

class BaseAppException(Exception):
    """Базовое исключение для нашего приложения"""
    def __init__(self, detail: str, status_code: int = 500):
        self.detail = detail
        self.status_code = status_code
        super().__init__(self.detail)


