from fastapi import APIRouter

from .delete_user import router as delete_user
from .get_user import router as get_user
from .update_user import router as update_user

router = APIRouter(
    tags=["User"],
)

router.include_router(delete_user)
router.include_router(get_user)
router.include_router(update_user)

