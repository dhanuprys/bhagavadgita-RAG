from abc import ABC, abstractmethod
from app.application.application_construct import (
    ApplicationConstruct,
    ApplicationContainer,
)
from fastapi import APIRouter


class Controller(ABC):
    @property
    @abstractmethod
    def router(self) -> APIRouter:
        pass

    def set_app(self, app: ApplicationConstruct, ctx: ApplicationContainer):
        self.app = app
        self.ctx = ctx
