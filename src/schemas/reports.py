from .base import BaseSchema
from src.types.status import StatusEnum


class ItemSchema(BaseSchema):
    id: int
    todo: str
    completed: bool


class TodosSchema(BaseSchema):
    total: int
    completed: int
    items: list[ItemSchema | None]


class UserSchema(BaseSchema):
    user_id: int
    user_name: str
    email: str

class ResultDataChema(BaseSchema):
    user: UserSchema
    todos: TodosSchema | None

class ResultSchema(BaseSchema):
    job_id: int
    status: str
    result: ResultDataChema

class ReportSchema(BaseSchema):
    job_id: int
    status: StatusEnum
