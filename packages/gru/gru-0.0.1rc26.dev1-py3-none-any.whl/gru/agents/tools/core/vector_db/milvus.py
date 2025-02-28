from pymilvus import connections, Collection
from typing import List, Dict, Any, Optional
from gru.agents.tools.core.vector_db.models import VectorDBConfig
from .base import VectorDBClient


class MilvusClient(VectorDBClient):
    def __init__(self):
        self.connection = None
        self.config = None

    def connect(self, config: VectorDBConfig) -> None:
        """Establishes a connection to the Milvus vector database."""
        connections.connect(
            alias="default",
            host=config.host,
            port=config.port
        )
        self.config = config  # Store the config for later use
        print("Connected to Milvus.")

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
        Performs a similarity search using the query vector
        and returns top-k results.
        """
        collection = Collection(collection_name)

        if search_params is None:
            search_params = {
                "metric_type": self.config.metric if self.config else "L2",
                "params": {
                    "nprobe": self.config.nprobe if self.config else 10
                },
            }

        # Perform the search
        results = collection.search(
            data=[query_vector],
            anns_field=anns_field,
            param=search_params,
            limit=top_k,
            output_fields=output_fields,
        )

        # Process and format the results
        search_results = []
        for hits in results:
            for hit in hits:
                result = {"score": hit.score}
                if output_fields:
                    for field in output_fields:
                        result[field] = hit.entity.get(field)
                search_results.append(result)

        return search_results

    async def filtered_search(
        self,
        collection_name: str,
        filter_expr: str,
        limit: int = 5,
        output_fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Performs a filtered search based on additional query parameters."""
        collection = Collection(collection_name)

        results = collection.query(
            expr=filter_expr, output_fields=output_fields, limit=limit
        )

        return results

    async def add_to_collection(
        self, collection_name: str, documents: List[Dict[str, Any]]
    ):
        raise NotImplementedError("Method not implemented yet")

    async def update_collection(
        self,
        collection_name: str,
        document_id: str,
        update_data: Dict[str, Any]
    ):
        raise NotImplementedError("Method not implemented yet")

    async def delete_from_collection(
        self,
        collection_name: str,
        document_id: str
    ):
        raise NotImplementedError("Method not implemented yet")

    async def list_collections(self) -> List[str]:
        raise NotImplementedError("Method not implemented yet")

    async def get_collection_stats(
        self,
        collection_name: str
    ) -> Dict[str, Any]:
        raise NotImplementedError("Method not implemented yet")

    async def reset_collection(self, collection_name: str):
        raise NotImplementedError("Method not implemented yet")
