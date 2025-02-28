from typing import Any, Dict, Optional
import uuid
import os

from gru.agents.framework_wrappers.memory.base import BaseMemory
from gru.agents.framework_wrappers.memory.collection_manager import CollectionManager
from gru.agents.tools.core.embeddings.embedding_factory import EmbeddingFactory, EmbeddingType
from datetime import datetime
from gru.agents.tools.core.vector_db.base import (
    AddToCollectionResponse,
    DeleteFromCollectionResponse,
    SimilaritySearchResponse,
    UpdateCollectionResponse
)
from gru.agents.tools.core.vector_db.vectordb_factory import VectorDBFactory, VectorDBType

class CansoMemory(BaseMemory):
    DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory_collections.yaml")


    def __init__(
        self,
        client: Any,
        embedding_type: str = EmbeddingType.OPENAI.value,
        vector_db_type: str = VectorDBType.MILVUS.value,
        config_path: Optional[str] = None,
    ):
        self.vdb_client = VectorDBFactory.get_vector_db_client(
            VectorDBType(vector_db_type) 
        )
        self.embedding_generator = EmbeddingFactory.get_embedding_generator(
            EmbeddingType(embedding_type),
            client
        )
        self.collection_schemas = {}

        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        
        self.collection_manager = CollectionManager(
            vector_db_client=self.vdb_client,
            embedding_dimension=self.embedding_generator.dimension,
            config_path=self.config_path
        )
        self.collection_manager.initialize_collections()

    async def store(self, data: Dict[str, Any], collection_name: str) -> AddToCollectionResponse:
        if not await self._validate_document_schema(data, collection_name):
            return AddToCollectionResponse(
                status="error",
                message=f"Document does not match schema for collection '{collection_name}'",
                ids=[]
            )
        
        text = data.get("text", "")
        if not text:
            return AddToCollectionResponse(
                status="error",
                message="Text field is required for embedding generation",
                ids=[]
            )
        
        try:
            embedding = await self.embedding_generator.generate(text)
        except Exception as e:
            return AddToCollectionResponse(
                status="error",
                message=f"Failed to generate embedding: {str(e)}",
                ids=[]
            )
        
        
        document = data.get("metadata", {}).copy()
        document["text"] = text
        
        if "id" not in document:
            document["id"] = str(uuid.uuid4())
        
        if "created_at" not in document:
            document["created_at"] = datetime.now().isoformat()
        
        result = await self.vdb_client.add_to_collection(
            collection_name,
            embeddings=[embedding],
            data=[document]
        )
        
        return AddToCollectionResponse(
            status="success" if result.status != "error" else "error",
            message=result.message,
            ids=result.ids
        )

    async def retrieve(
            self, 
            query: str, 
            collection_name: str,
            top_k: int = 5
        ) -> SimilaritySearchResponse:
        try:
            query_embedding = await self.embedding_generator.generate(query)
            results = await self.vdb_client.similarity_search(
                collection_name=collection_name,
                query_vector=query_embedding,
                top_k=top_k,
            )
            return results
        except Exception as e:
            print(f"Error in retrieve: {str(e)}")
            return SimilaritySearchResponse(
                status="error",
                message=f"Failed to retrieve documents: {str(e)}",
                results=[]
            )

    async def update(
            self,
            doc_id: str,
            data: Dict[str, Any],
            collection_name: str
    ) -> UpdateCollectionResponse:
        """Update an existing memory entry in specified collection"""
        try:
            text = data.get("text")
            if text is None:
                raise ValueError("Text content is required for update")

            embedding = await self.embedding_generator.generate(text)

            # Prepare metadata with all necessary fields
            metadata = {
                "text": text,
                "metadata": data.get("metadata", {}),
                "created_at": datetime.now().isoformat()
            }

            result = await self.vdb_client.update_collection(
                collection_name=collection_name,
                memory_id=doc_id,
                embedding=embedding,
                metadata=metadata
            )

            return result
        except Exception as e:
            return UpdateCollectionResponse(
                status="error",
                message=f"Failed to update document: {str(e)}",
                id=doc_id,
                updated_count=None
            )

    async def delete(
            self, 
            doc_id: str,
            collection_name: str
        ) -> DeleteFromCollectionResponse:
        """Delete a memory entry from specified collection"""
        return await self.vdb_client.delete_from_collection(
            collection_name=collection_name,
            memory_id=doc_id
        )

    async def _validate_document_schema(self, data: Dict[str, Any], collection_name: str) -> bool:

        schema = await self._get_collection_info(collection_name)
        if not schema:
            return False
        
        fields = schema.get("fields", [])
        if not fields:
            return True  
        
        field_dict = {field.get("name"): field for field in fields}
        
        for field_name, field_value in data.items():
            if field_name not in field_dict:
                continue  
                
            field_info = field_dict[field_name]
            field_type = field_info.get("dtype")
            
            if field_type == "VARCHAR" and isinstance(field_value, str):
                max_length = field_info.get("max_length")
                if max_length and len(field_value) > max_length:
                    print(f"Field '{field_name}' exceeds maximum length of {max_length}")
                    return False
            
        primary_fields = [field.get("name") for field in fields if field.get("is_primary")]
        for primary_field in primary_fields:
            if primary_field not in data:
                if primary_field != "id":
                    print(f"Missing primary key '{primary_field}' for collection '{collection_name}'")
                    return False
        
        return True

    async def _get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        try:
            collections = await self.vdb_client.list_collections()
            if collection_name not in collections.collections:
                raise ValueError("Collection not found")
            
            collection_info = await self.vdb_client.get_collection_info(collection_name)
            if collection_info.status == "error":
                raise ValueError("Error getting collection info")
            
            fields = collection_info.collection_info.get("fields", [])
            
            schema = {
                "name": collection_name,
                "fields": fields,
                "description": collection_info.collection_info.get("description", ""),
            }
            
            indexes = collection_info.collection_info.get("indexes", [])
            if indexes:
                schema["index_params"] = {
                    index.get("field_name"): {
                        "index_type": index.get("index_type", ""),
                        "params": index.get("params", {})
                    }
                    for index in indexes
                }
            
            return schema
        except Exception as e:
            print(f"Error fetching collection schema from Milvus: {str(e)}")
            raise e
        
