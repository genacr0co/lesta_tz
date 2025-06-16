from fastapi import APIRouter

from .get_collections import router as get_collections
from .create_collection import router as create_collection
from .delete_collection import router as delete_collection
from .get_collection_id import router as get_collection_id
from .get_collection_statistics import router as get_collection_statistics

from .add_document_to_collection import router as add_document_to_collection
from .remove_document_from_collection import router as remove_document_from_collection

router = APIRouter(
    tags=["Collections"],
)

router.include_router(get_collections)
router.include_router(create_collection)
router.include_router(delete_collection)
router.include_router(get_collection_id)
router.include_router(get_collection_statistics)
router.include_router(add_document_to_collection)
router.include_router(remove_document_from_collection)



