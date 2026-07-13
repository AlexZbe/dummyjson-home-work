from fastapi import APIRouter, Request

from api.dep import DBDep
from src.exceptions.exceptions_http import ExternalHTTPError, NotFoundHTTPExceprion
from src.services.reports import ReportService
from src.exceptions.exceptions_service import ExternalServiceError, NotFoundServiceExceprion
from src.schemas.reports import ReportSchema, ResultSchema
from src.utils.task_runner import ThreadReportTaskRunner

router = APIRouter()


@router.post("/reports/{user_id}")
async def create_report(
    user_id: int, db: DBDep, requests: Request
) -> ReportSchema:
    task_runner = ThreadReportTaskRunner(requests.app.state.thread_pool)
    try:
        return await ReportService(db, task_runner=task_runner).create(user_id)
    except NotFoundServiceExceprion:
        raise NotFoundHTTPExceprion(user_id)
    except ExternalServiceError as err:
        raise ExternalHTTPError(err.message)


@router.get("/reports/jobs/{job_id}")
async def get_job_by_id(job_id: int, db: DBDep, requests: Request) -> ResultSchema:
    try:
        result = await ReportService(db).get_job_by_id(job_id)
    except ExternalServiceError as err:
        raise ExternalHTTPError(err.message)


    if not result:
        raise NotFoundHTTPExceprion(job_id)

    return result


@router.get("/ping")
async def ping():
    return dict(status="ok")
