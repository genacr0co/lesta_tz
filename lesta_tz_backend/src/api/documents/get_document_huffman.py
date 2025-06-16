from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pathlib import Path as FilePath
import re
import time
import heapq
from collections import Counter

from src.db import get_async_session
from src.utils import check_user_access
from src.models import Document
from src.api.meta import update_metrics

from .schemas import HuffmanResponse, CodeItem

router = APIRouter()
http_bearer = HTTPBearer()
class HuffmanNode:
    def __init__(self, word=None, freq=0):
        self.word = word
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def tokenize_stream(file_path: str):
    pattern = re.compile(r'\b\w+\b')
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            yield from pattern.findall(line.lower())


def count_frequencies(file_path: str) -> Counter:
    freq = Counter()
    for word in tokenize_stream(file_path):
        freq[word] += 1
    return freq


def build_huffman_tree(freq: Counter) -> HuffmanNode:
    heap = [HuffmanNode(word, f) for word, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(freq=node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)

    return heap[0] if heap else None


def build_codes(node: HuffmanNode, prefix="", code_map=None):
    if code_map is None:
        code_map = {}

    if node.word is not None:
        code_map[node.word] = prefix
    else:
        if node.left:
            build_codes(node.left, prefix + "0", code_map)
        if node.right:
            build_codes(node.right, prefix + "1", code_map)
    return code_map


def huffman_encode_file(file_path: str):
    freq = count_frequencies(file_path)
    if not freq:
        return {"encoded": "", "codes": {}, "original_length": 0, "encoded_length": 0}

    root = build_huffman_tree(freq)
    codes = build_codes(root)

    words = list(tokenize_stream(file_path))
    encoded_str = "".join(codes[word] for word in words)

    return {
        "encoded": encoded_str,
        "codes": codes,
        "original_length": len(words),
        "encoded_length": len(encoded_str)
    }


@router.get("/documents/{document_id}/huffman", response_model=HuffmanResponse)
async def get_huffman_encoded_document(
    document_id: int = Path(..., ge=1),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session)
) -> HuffmanResponse:
    user = await check_user_access(token, session)

    stmt = select(Document).where(Document.id == document_id, Document.owner_id == user.id)
    result = await session.execute(stmt)
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")

    file_path = FilePath(document.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=500, detail="Файл не найден на сервере")

    try:
        start_time = time.perf_counter()
        encoded_data = huffman_encode_file(str(file_path))
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        codes_list = [CodeItem(text=word, code=code) for word, code in encoded_data["codes"].items()]

        file_size = file_path.stat().st_size

        # Обновляем метрики
        await update_metrics(
            session=session,
            time_taken=elapsed_time,
            user_id=user.id,
            user_name=user.name,
            file_size=file_size,
            file_name=file_path.name,
            file_path=str(file_path)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при кодировании: {str(e)}")

    return HuffmanResponse(
        encoded=encoded_data["encoded"],
        codes=codes_list,
        original_length=encoded_data["original_length"],
        encoded_length=encoded_data["encoded_length"]
    )