from fastapi import APIRouter

from .delete_document import router as delete_document
from .get_document_statistics import router as get_document_statistics
from .get_document_id import router as get_document_id
from .upload_document import router as upload_document
from .get_document_huffman import router as get_document_huffman
from .get_documents import router as get_documents


router = APIRouter(
    tags=["Documents"],
)

router.include_router(delete_document)
router.include_router(get_document_statistics)
router.include_router(get_document_id)
router.include_router(upload_document)
router.include_router(get_document_huffman)
router.include_router(get_documents)

