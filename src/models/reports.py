from sqlalchemy import Integer, String
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.types.status import StatusEnum

from .base import BaseModel


class ReportsModel(BaseModel):
    __tablename__: str = "report"

    job_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer())
    user_name: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String())
    status: Mapped[str] = mapped_column(String(), default=StatusEnum.running.value)
    todos: Mapped[dict | None] = mapped_column(JSON(), default=None)
