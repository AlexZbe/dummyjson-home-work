from integrations.dummyjson import DummyJsonClient
from src.api.dep import DBDep
from src.exceptions.exceptions_service import NotFoundServiceExceprion
from src.schemas.reports import ReportSchema, ResultSchema
from src.utils.task_runner import TaskRunner

from .base import BaseService


class ReportService(BaseService):
    def __init__(self, db: DBDep, task_runner: TaskRunner | None = None):
        self.task_runner = task_runner
        super().__init__(db)

    async def create(self, user_id: int) -> ReportSchema:
        user = await DummyJsonClient().get_user(user_id)

        if not user:
            raise NotFoundServiceExceprion(user_id)

        report = await self.db.reports.create(user)
        if self.task_runner:
            self.task_runner.run(
                task=DummyJsonClient().get_user_todos_sync,
                job_id=report.job_id,
                user_id=user.user_id,
            )
        return report

    async def get_job_by_id(self, job_id: int) -> ResultSchema | None:
        return await self.db.reports.get_job_by_id(job_id)
