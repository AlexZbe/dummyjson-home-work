from api.dep import DBDep


class BaseService:
    def __init__(self, db: DBDep):
        self.db = db
