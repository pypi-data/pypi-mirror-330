from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from gru.agents.tools.core.vector_db.base import VectorDBClient
from gru.agents.tools.core.code_generator.models import RetrievalResult


class ContextRetriever(ABC):
    def __init__(
        self,
        vector_store: VectorDBClient,
        system_prompt: Optional[str] = None,
        user_prompt_template: Optional[str] = None,
    ):
        """
        Base class for Context Retrievers.
        """
        self.vector_store = vector_store
        self.system_prompt = system_prompt
        self.user_prompt_template = user_prompt_template

    @abstractmethod
    async def get_relevant_datasources_and_schemas(
        self,
        query_embedding: List[float],
        top_k: int,
        embedding_field: str,
        search_params: Optional[Dict[str, Any]] = None,
        output_fields: Optional[List[str]] = None,
    ) -> Tuple[List[str], List[str]]:
        """
        Retrieves relevant data sources and their schemas.
        """
        pass

    @abstractmethod
    async def get_similar_examples(
        self,
        query_embedding: List[float],
        top_k: int,
        embedding_field: str,
        search_params: Optional[Dict[str, Any]] = None,
        output_fields: Optional[List[str]] = None,
    ) -> List[str]:
        """Retrieves similar examples based on the query embedding."""
        pass

    @abstractmethod
    async def get_documentation(
        self,
        query_embedding: List[float],
        top_k: int,
        embedding_field: str,
        search_params: Optional[Dict[str, Any]] = None,
        output_fields: Optional[List[str]] = None,
    ) -> List[str]:
        """Retrieves relevant documentation based on the query embedding."""
        pass

    @abstractmethod
    async def retrieve_context(
        self, query_embedding: List[float], top_k: int
    ) -> RetrievalResult:
        """Retrieves all relevant context for the query embedding."""
        pass
