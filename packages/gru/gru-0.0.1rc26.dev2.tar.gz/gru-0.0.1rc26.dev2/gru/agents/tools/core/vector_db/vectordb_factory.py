from enum import Enum
from gru.agents.tools.core.vector_db.milvus import MilvusClient
from gru.agents.tools.core.vector_db.base import VectorDBClient

class VectorDBType(Enum):
    """Enum for supported vector database types"""
    MILVUS = "milvus"

class VectorDBFactory:
    """Factory class for creating vector database clients"""
    @staticmethod
    def get_vector_db_client(
        vector_db_type: VectorDBType, 
    ) -> VectorDBClient:
        """
        Create a vector database client based on the specified type.
        
        Args:
            vector_db_type: Type of vector database to create
            **kwargs: Additional arguments to pass to the constructor
            
        Returns:
            An instance of the requested VectorDBClient
        """
        if vector_db_type == VectorDBType.MILVUS:
            return MilvusClient()
        else:
            raise ValueError(f"Unsupported vector database type: {vector_db_type}")
