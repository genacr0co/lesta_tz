from pydantic import BaseModel
from typing import List
from pydantic import ConfigDict

class UploadResponse(BaseModel):
    message: str
    document_id: int


class WordStatistic(BaseModel):
    word: str
    tf: float
    idf: float

    model_config = ConfigDict(from_attributes=True)

class DocumentStatisticsResponse(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    results: List[WordStatistic]

    model_config = ConfigDict(from_attributes=True)


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

class PaginatedDocumentsResponse(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    documents: List[DocumentResponse]

    model_config = ConfigDict(from_attributes=True)