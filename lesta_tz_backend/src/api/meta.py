from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.config import APP_VERSION

router = APIRouter()

@router.get("/status")
async def health_check():
    return JSONResponse(content={"status": "OK"})


@router.get("/version")
async def get_version():
    return JSONResponse(content={"version": APP_VERSION})


# @router.get("/metrics")
# async def metrics(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
#     return {"Status":"OK"}
