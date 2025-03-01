from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class VectorDBConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    connection_timeout: int
    max_retries: int

class CreateCollectionResponse(BaseModel):
    status: str
    message: str
    collection_name: str

class AddToCollectionResponse(BaseModel):
    status: str
    message: str
    ids: List[str]

class UpdateCollectionResponse(BaseModel):
    status: str
    message: str
    id: str
    updated_count: Optional[int] = None

class DeleteFromCollectionResponse(BaseModel):
    status: str
    message: str

class SimilaritySearchResponse(BaseModel):
    status: str
    message: str
    results: List[Dict[str, Any]]

class ListCollectionsResponse(BaseModel):
    status: str
    message: str
    collections: List[str]

class GetCollectionInfoResponse(BaseModel):
    status: str
    message: str
    collection_info: Dict[str, Any]

class DropCollectionResponse(BaseModel):
    status: str
    message: str

class VectorDBClient(ABC):
    @abstractmethod
    def connect(self, config: VectorDBConfig) -> None:
        """Initialize connection to vector database"""
        pass

    @abstractmethod
    def create_collection_sync(
        self,
        collection_name: str,
        schema: Dict[str, Any],
        replace_existing: bool = False
    ) -> CreateCollectionResponse:
        """Create a new collection with specified schema synchronously"""
        pass

    @abstractmethod
    async def create_collection(
        self,
        collection_name: str,
        schema: Dict[str, Any],
        replace_existing: bool = False
    ) -> CreateCollectionResponse:
        """Create a new collection with specified schema asynchronously"""
        pass

    @abstractmethod
    async def add_to_collection(
        self, 
        collection_name: str, 
        embeddings: List[List[float]], 
        data: List[Dict[str, Any]]
    ) -> AddToCollectionResponse:
        """Add documents with embeddings to collection"""
        pass

    @abstractmethod
    async def update_collection(
        self, 
        collection_name: str, 
        memory_id: str, 
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> UpdateCollectionResponse:
        """Update document in collection"""
        pass

    @abstractmethod
    async def delete_from_collection(
        self, 
        collection_name: str, 
        memory_id: str
    ) -> DeleteFromCollectionResponse:
        """Delete document from collection"""
        pass

    @abstractmethod
    async def similarity_search(
        self,
        collection_name: str,
        query_vector: List[float],
        anns_field: Optional[str] = None,
        top_k: int = 5,
        search_params: Optional[Dict[str, Any]] = None,
        output_fields: Optional[List[str]] = None,
    ) -> SimilaritySearchResponse:
        """Search for similar vectors in collection"""
        pass

    @abstractmethod
    async def filtered_search(
        self,
        collection_name: str,
        filter_expr: str,
        limit: int = 5,
        output_fields: Optional[List[str]] = None,
    ) -> SimilaritySearchResponse:
        """Performs a filtered search based on additional query parameters."""
        pass

    @abstractmethod
    async def list_collections(self) -> ListCollectionsResponse:
        """List all available collections"""
        pass

    @abstractmethod
    async def get_collection_info(
        self, 
        collection_name: str
    ) -> GetCollectionInfoResponse:
        """Get collection metadata and statistics"""
        pass

    @abstractmethod
    async def drop_collection(
        self, 
        collection_name: str
    ) -> DropCollectionResponse:
        """Delete an entire collection"""
        pass