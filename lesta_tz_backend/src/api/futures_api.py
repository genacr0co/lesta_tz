import math
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session

router = APIRouter()

http_bearer = HTTPBearer()



@router.get("/status")
async def get_status(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}


@router.get("/metrics")
async def metrics(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}


@router.get("/version")
async def version(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}


@router.get("/collections")
async def collection_list(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}

@router.get("/collections/{collection_id}")
async def get_collection(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}

@router.get("/collections/{collection_id}/statistics")
async def get_collection_statistics(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}



@router.post("/collection/{collection_id}/{document_id}")
async def add_document_to_collection(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}

@router.delete("/collection/{collection_id}/{document_id}")
async def delete_document_from_collection(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}


@router.get("/logout")
async def logout(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}

@router.get("/user")
async def get_user(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}


@router.patch("/user/{user_id}")
async def update_user_data(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}

@router.delete ("/user/{user_id}")
async def delete_user_data(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}


@router.get("/documents/{document_id}/huffman")
async def document_huffman(token: str = Depends(http_bearer), session: AsyncSession = Depends(get_async_session)) -> dict:
    return {"Status":"OK"}