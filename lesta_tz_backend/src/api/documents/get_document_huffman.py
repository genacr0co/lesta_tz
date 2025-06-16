from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pathlib import Path as FilePath
import re

import heapq
from collections import Counter

from src.db import get_async_session
from src.utils import check_user_access
from src.models import Document

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


def tokenize(text: str) -> list[str]:
    # Разделяет на слова с учётом пунктуации
    return re.findall(r'\b\w+\b', text.lower())


def build_huffman_tree(words: list[str]) -> HuffmanNode:
    frequency = Counter(words)
    heap = [HuffmanNode(word, freq) for word, freq in frequency.items()]
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


def huffman_encode(text: str) -> dict:
    words = tokenize(text)
    if not words:
        return {"encoded": "", "codes": {}, "original_words": []}

    root = build_huffman_tree(words)
    codes = build_codes(root)
    encoded = "".join(codes[word] for word in words)
    
    return {
        "encoded": encoded,
        "codes": codes,
        "original_length": len(words),
        "encoded_length": len(encoded),
    }


@router.get("/documents/{document_id}/huffman")
async def get_huffman_encoded_document(
    document_id: int = Path(..., ge=1),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session)
):
    user = await check_user_access(token, session)

    stmt = select(Document).where(Document.id == document_id, Document.owner_id == user.id)
    result = await session.execute(stmt)
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")

    try:
        with open(FilePath(document.file_path), "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Файл не найден на сервере")

    encoded_data = huffman_encode(text)

    return {
        "encoded": encoded_data["encoded"],
        "codes": encoded_data["codes"],
        "original_length": encoded_data["original_length"],  # <= правильно
        "encoded_length": encoded_data["encoded_length"]
    }