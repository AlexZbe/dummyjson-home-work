from typing import Any

from fastapi import HTTPException


class BaseHTTPExceprion(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)


class NotFoundHTTPExceprion(BaseHTTPExceprion):
    def __init__(self, id: Any) -> None:
        self.detail = f"Запись с идентификатором {str(id)!r} не найдена"
        self.status_code=404
        super().__init__(detail=self.detail, status_code=self.status_code)


class ExternalHTTPError(BaseHTTPExceprion):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=500, detail=detail)
