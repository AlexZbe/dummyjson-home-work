import asyncio
from httpx import AsyncClient
import httpx

from src.exceptions.exceptions_service import BaseServiceExceprion, ExternalServiceError
from src.integrations.legacy.legacy_client import get_user_todos_sync
from src.schemas.reports import UserSchema
from src.core.db_manager import SessionManager, async_session_factory


class DummyJsonClient:

    servise_name: str = "dummyjson.com"

    def __init__(self):
        pass

    async def get_user(self, user_id: int) -> UserSchema | None:
        async with AsyncClient() as client:
            try:
                timeout = httpx.Timeout(
                    connect=15,
                    read=3,
                    write=3,
                    pool=3,
                )
                result = await client.get(f"https://dummyjson.com/users/{user_id}", timeout=timeout)
            except httpx.ConnectTimeout:
                raise ExternalServiceError(service_name=self.servise_name)
            except Exception:
                raise ExternalServiceError(service_name=self.servise_name, message="Неизвестная ошибка внешнего сервиса")
            if result.status_code == 404:
                return None

            result_dict = result.json()

            user = UserSchema(
                email=result_dict["email"],
                user_id=user_id,
                user_name=result_dict["firstName"],
            )

            return user

    def get_user_todos_sync(self, user_id: int, job_id: int):
        async def wrapper():
            async with SessionManager(async_session_factory) as db:
                try:
                    try:
                        response = get_user_todos_sync(user_id=user_id)
                    except httpx.ConnectTimeout:
                        raise ExternalServiceError(service_name=self.servise_name)
                    except Exception:
                        raise ExternalServiceError(service_name=self.servise_name, message="Неизвестная ошибка внешнего сервиса")
                except BaseServiceExceprion:
                    await db.reports.write_status_error(job_id)
                    raise


                result = self.__formated_todos(response)
                await db.reports.add_todos(result, job_id)



        asyncio.run(wrapper())


    def __formated_todos(self, data: dict) -> dict:
        result = dict()

        result["total"] = data["total"]
        result["items"] = data["todos"]
        count_completed = 0
        for item in result["items"]:
            if item["completed"]:
                count_completed += 1

        result["completed"] = count_completed
        return result
