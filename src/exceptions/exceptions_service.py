from typing import Any


class BaseServiceExceprion(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NotFoundServiceExceprion(BaseServiceExceprion):
    def __init__(self, name: Any) -> None:
        self.message = f"Запись с идентификатором {str(name)!r} не найдена"
        super().__init__(self.message)


class ExternalServiceError(BaseServiceExceprion):
    def __init__(
        self,
        service_name: str,
        message: str = "Внешний сервис временно недоступен",
    ) -> None:
        self.service_name = service_name
        self.message = f"{message}: {service_name}"

        super().__init__(message)
