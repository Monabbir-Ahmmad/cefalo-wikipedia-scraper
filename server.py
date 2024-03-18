from fastapi import FastAPI
from app.api.v1.route import router as v1_router
from app.core.config import Config
from app.utils.decorator import singleton
from app.core.factory import AppFactory

@singleton
class AppCreator:
    def __init__(self):
        self.app = FastAPI(
            title=Config.PROJECT_NAME,
            openapi_url=f"{Config.API}/openapi.json",
            version="0.0.1",
        )

        self.factory = AppFactory()
        
        @self.app.get("/")
        def root():
            return "Service is working"

        self.app.include_router(v1_router, prefix=Config.API_V1_STR)


app_creator = AppCreator()
app = app_creator.app