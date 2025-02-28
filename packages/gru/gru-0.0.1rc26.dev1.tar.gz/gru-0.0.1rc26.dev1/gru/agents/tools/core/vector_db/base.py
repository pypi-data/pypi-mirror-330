from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from gru.agents.tools.core.vector_db.models import VectorDBConfig


class VectorDBClient(ABC):
    @abstractmethod
    def connect(self, config: VectorDBConfig) -> None:
        """Establishes a connection to the vector database."""
        pass

    @abstractmethod
    async def similarity_search(
        self,
        collection_name: str,
        query_vector: List[float],
        anns_field: str,
        top_k: int = 5,
        search_params: Optional[Dict[str, Any]] = None,
        output_fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Performs a similarity search using the query and returns top-k results.
        """
        pass

    @abstractmethod
    async def filtered_search(
        self,
        collection_name: str,
        filter_expr: str,
        limit: int = 5,
        output_fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Performs a filtered search based on additional query parameters."""
        pass

    @abstractmethod
    async def add_to_collection(
        self, collection_name: str, documents: List[Dict[str, Any]]
    ):
        """Adds new documents to the vector database collection."""
        pass

    @abstractmethod
    async def update_collection(
        self,
        collection_name: str,
        document_id: str,
        update_data: Dict[str, Any]
    ):
        """Updates an existing document in the specified collection."""
        pass

    @abstractmethod
    async def delete_from_collection(
        self,
        collection_name: str,
        document_id: str
    ):
        """Deletes a document from the specified collection."""
        pass

    @abstractmethod
    async def list_collections(self) -> List[str]:
        """
        Lists all available collections in the vector database.
        """
        pass

    @abstractmethod
    async def get_collection_stats(
        self,
        collection_name: str
    ) -> Dict[str, Any]:
        """Returns statistics for a given collection."""
        pass

    @abstractmethod
    async def reset_collection(self, collection_name: str):
        """Clears all data from the specified collection."""
        pass
