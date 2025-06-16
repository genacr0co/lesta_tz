from fastapi import APIRouter

from .auth.routers import router as auth_routers
from .user.routers import router as user_routers
from .collections.routers import router as collections_routers
from .documents.routers import router as documents_routers
from .meta import router as status_routers


api = APIRouter(
    prefix="/api/v1",
)

api.include_router(auth_routers)
api.include_router(user_routers)
api.include_router(collections_routers)
api.include_router(documents_routers)
api.include_router(status_routers)

