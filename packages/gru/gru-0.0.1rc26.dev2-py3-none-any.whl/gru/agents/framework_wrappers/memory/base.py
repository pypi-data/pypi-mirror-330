from abc import ABC, abstractmethod
from typing import Any, Dict

from gru.agents.tools.core.vector_db.base import (
    AddToCollectionResponse,
    DeleteFromCollectionResponse,
    UpdateCollectionResponse,
    SimilaritySearchResponse
)


class BaseMemory(ABC):
    """Base class for memory implementations"""

    @abstractmethod
    async def store(self, data: Dict[str, Any], collection_name: str) -> AddToCollectionResponse:
        """Store data in specified collection"""
        pass

    @abstractmethod
    async def retrieve(
        self, 
        query: str, 
        collection_name: str,
        top_k: int = 5
    ) -> SimilaritySearchResponse:
        """Retrieve data from specified collection based on query"""
        pass

    @abstractmethod
    async def update(
        self, 
        doc_id: str, 
        data: Dict[str, Any],
        collection_name: str
    ) -> UpdateCollectionResponse:
        """Update existing data in specified collection"""
        pass

    @abstractmethod
    async def delete(
        self, 
        doc_id: str,
        collection_name: str
    ) -> DeleteFromCollectionResponse:
        """Delete data from specified collection"""
        pass