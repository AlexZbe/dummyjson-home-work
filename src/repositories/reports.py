from src.exceptions.exceptions_service import NotFoundServiceExceprion
from src.models.reports import ReportsModel
from src.repositories.base import BaseRepository
from src.schemas.reports import ReportSchema, ResultDataChema, ResultSchema, TodosSchema, UserSchema
from src.types.status import StatusEnum


class ReportRepository(BaseRepository):
    async def create(self, user: UserSchema) -> ReportSchema:
        report_running = ReportsModel(**user.model_dump())
        self.session.add(report_running)
        await self.session.commit()
        await self.session.refresh(report_running)
        return ReportSchema(
            job_id=report_running.job_id,
            status=report_running.status, # pyright: ignore[reportArgumentType]
        )

    async def add_todos(self, todos: dict, job_id: int) -> None:
        report = await self.session.get(ReportsModel, job_id)
        if not report:
            raise NotFoundServiceExceprion(f"{job_id=}")
        report.todos = todos
        report.status = StatusEnum.done.value
        await self.session.commit()

    async def write_status_error(self, job_id: int) -> None:
        report = await self.session.get(ReportsModel, job_id)
        if not report:
            raise NotFoundServiceExceprion(f"{job_id=}")
        report.status = StatusEnum.error.value
        await self.session.commit()

    async def get_job_by_id(self, job_id: int) -> ResultSchema | None:
        report = await self.session.get(ReportsModel, job_id)

        if not report:
            return None
        user = UserSchema(
            email=report.email,
            user_id=report.user_id,
            user_name=report.user_name
        )

        if report.status == StatusEnum.done.value:
            todos = TodosSchema(**report.todos) # pyright: ignore[reportCallIssue]
        else:
            todos = None

        return ResultSchema(
            job_id=report.job_id,
            status=report.status,
            result=ResultDataChema(
                user=user,
                todos=todos
            )
        )
