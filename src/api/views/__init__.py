from fastapi import APIRouter

api_router = APIRouter(prefix="/api")

api_router_v1 = APIRouter(prefix="/v1")

api_router.include_router(api_router_v1)
