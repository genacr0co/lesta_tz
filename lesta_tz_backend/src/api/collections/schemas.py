from pydantic import BaseModel
from typing import List


class WordStatistic(BaseModel):
    word: str
    tf: float
    idf: float

class DocumentStatisticsResponse(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    results: List[WordStatistic]


class CollectionResponse(BaseModel):
    id: int
    name: str

class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    owner_id: int

class PaginatedDocumentsResponse(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    documents: List[DocumentResponse]

class CollectionListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    results: List[CollectionResponse]