from typing import Generator
from fastapi import FastAPI
from fastapi.security import HTTPBasic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from nephyx.core.settings import BaseSettings
from nephyx.router import ApiRouter


class NephyxApi:
    def __init__(self, settings_cls: type[BaseSettings] = BaseSettings):
        self.settings = settings_cls()
        self.fastapi_app = FastAPI()

        self._setup_database()
        self._setup_basic_auth()

    def _setup_database(self):
        self.db_engine = create_engine(str(self.settings.database_url))
        self._session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self.db_engine)

    def _setup_basic_auth(self):
        self.fastapi_app.state.basic_auth = HTTPBasic()

    def include_router(self, router: ApiRouter):
        self.fastapi_app.include_router(router)
        router.set_app_dependency(lambda: self)

    def get_db(self) -> Generator[Session, None, None]:
        db = self._session_factory()
        try:
            yield db
        finally:
            db.close()
