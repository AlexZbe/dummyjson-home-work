from typing import Annotated
from fastapi import Depends

from src.core.db_manager import SessionManager, get_db


DBDep = Annotated[SessionManager, Depends(get_db)]
