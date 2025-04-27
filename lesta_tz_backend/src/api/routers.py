from fastapi import APIRouter

from .delete_document import router as delete_router
from .documents import router as documents_router
from .get_document import router as get_document_router
from .upload_document import router as upload_document_router


api = APIRouter(
    prefix="/api",
    tags=["Lesta TF_IDF API"],
)

api.include_router(upload_document_router)
api.include_router(documents_router)
api.include_router(get_document_router)
api.include_router(delete_router)

