from typing import List, Dict, Any, Optional, Tuple
from gru.agents.tools.core.code_generator.models import RetrievalResult
from gru.agents.tools.core.vector_db.milvus import MilvusClient
from .base import ContextRetriever


class SQLContextRetriever(ContextRetriever):
    def __init__(
        self,
        vector_store: MilvusClient,
        system_prompt: Optional[str] = None,
        user_prompt_template: Optional[str] = None,
    ):
        super().__init__(vector_store, system_prompt, user_prompt_template)
        self.vector_store = vector_store

    async def get_relevant_datasources_and_schemas(
        self,
        query_embedding: List[float],
        top_k: int,
        embedding_field: str,
        search_params: Optional[Dict[str, Any]] = None,
        output_fields: Optional[List[str]] = None,
    ) -> Tuple[List[str], List[str]]:
        """
        Retrieves relevant data sources (tables) and their schemas.
        """
        if search_params is None:
            search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

        if output_fields is None:
            output_fields = ["table_name", "contents"]

        results = await self.vector_store.similarity_search(
            collection_name="table_metadatas",
            query_vector=query_embedding,
            anns_field=embedding_field,
            top_k=top_k,
            search_params=search_params,
            output_fields=output_fields,
        )

        tables = [result.get("table_name", "") for result in results]
        schemas = [result.get("contents", "") for result in results]

        return tables, schemas

    async def get_similar_examples(
        self,
        query_embedding: List[float],
        top_k: int,
        embedding_field: str,
        search_params: Optional[Dict[str, Any]] = None,
        output_fields: Optional[List[str]] = None,
    ) -> List[str]:
        """Retrieves similar examples based on the query embedding."""
        if output_fields is None:
            output_fields = ["examples"]

        results = await self.vector_store.similarity_search(
            collection_name="example_queries",
            query_vector=query_embedding,
            anns_field=embedding_field,
            top_k=top_k,
            search_params=search_params,
            output_fields=output_fields,
        )
        return [result.get("examples", "") for result in results]

    async def get_documentation(
        self,
        query_embedding: List[float],
        top_k: int,
        embedding_field: str,
        search_params: Optional[Dict[str, Any]] = None,
        output_fields: Optional[List[str]] = None,
    ) -> List[str]:
        """Retrieves relevant documentation based on the query embedding."""
        if output_fields is None:
            output_fields = ["documentation"]

        results = await self.vector_store.similarity_search(
            collection_name="table_documentation",
            query_vector=query_embedding,
            anns_field=embedding_field,
            top_k=top_k,
            search_params=search_params,
            output_fields=output_fields,
        )
        return [result.get("documentation", "") for result in results]

    async def retrieve_context(
        self, query_embedding: List[float], top_k: int
    ) -> RetrievalResult:
        """Retrieves all relevant context for the query embedding."""
        tables, schemas = await self.get_relevant_datasources_and_schemas(
            query_embedding, top_k, "embedding"
        )
        examples = await self.get_similar_examples(
            query_embedding,
            top_k,
            "embeddings"
        )
        documentation = await self.get_documentation(
            query_embedding, top_k, "embeddings"
        )

        return RetrievalResult(
            tables=tables,
            schemas=schemas,
            documentation=documentation,
            examples=examples,
            low_cardinality_values=[],
            domain_knowledge=[],
            opt_rules=[],
        )
