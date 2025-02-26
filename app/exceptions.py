from fastapi import HTTPException


class ServiceException(HTTPException):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail

class SQLException(ServiceException):
    def __init__(self, status_code = 400, detail = 'Возникла ошибка'):
        self.status_code = status_code
        self.detail = detail