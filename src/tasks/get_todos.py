from integrations.legacy.legacy_client import get_user_todos_sync


def task_get_todos(user_id: int):

    result = get_user_todos_sync(user_id=user_id)
