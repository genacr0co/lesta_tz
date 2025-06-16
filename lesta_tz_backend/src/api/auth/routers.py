from fastapi import APIRouter

from .register import router as register
from .login import router as login
from .logout import router as logout
from .refresh import router as refresh

router = APIRouter(
    tags=["Auth"],
)

router.include_router(register)
router.include_router(login)
router.include_router(logout)
router.include_router(refresh)


