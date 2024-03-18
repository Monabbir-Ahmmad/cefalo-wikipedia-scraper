from fastapi import APIRouter
from app.api.v1.endpoints import movie

router = APIRouter()

router_list = [movie.router]

for router in router_list:
    router.include_router(router)