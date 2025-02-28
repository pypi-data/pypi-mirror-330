import os
import yaml
from typing import Dict, Any, List, Optional

from gru.agents.tools.core.vector_db.base import VectorDBClient

class CollectionManager:
    """
    Manages vector database collections, handling initialization and schema management.
    This class extracts collection handling logic from CansoMemory for better separation
    of concerns and readability.
    """
    
    def __init__(self, vector_db_client: VectorDBClient, embedding_dimension: int, config_path: Optional[str] = None):
        """
        Initialize the collection manager.
        
        Args:
            vector_db_client: The vector database client to use
            embedding_dimension: Dimension for embedding vectors
            config_path: Path to collections configuration file
        """
        self.vdb_client = vector_db_client
        self.embedding_dimension = embedding_dimension
        self.config_path = config_path
        self.collections_config = self._load_config()
        
    def _load_config(self) -> Optional[Dict[str, Any]]:
        """Load collections configuration from YAML file"""
        if not self.config_path or not os.path.exists(self.config_path):
            return None
            
        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file)
            print(f"Loaded collections config from {self.config_path}")
            return config
    
    def initialize_collections(self) -> None:
        """Initialize collections defined in the configuration file"""
        if not self.collections_config:
            print("No collections configuration found")
            return

        collections = self.collections_config.get("collections", {})
        print(f"Initializing {len(collections)} collections")
        
        for collection_name, collection_config in collections.items():
            try:
                print(f"Creating collection: {collection_name}")
                schema = self._build_collection_schema(collection_config)
                
                replace_existing = collection_config.get("replace_existing", False)
                
                self.vdb_client.create_collection_sync(
                    collection_name=collection_name,
                    schema=schema,
                    replace_existing=replace_existing
                )
            except Exception as e:
                print(f"Warning: Failed to create collection {collection_name}: {str(e)}")
    
    def _build_collection_schema(self, collection_config: Dict[str, Any]) -> Dict[str, Any]:
        """Build schema for a collection based on configuration"""
        fields = self._prepare_fields(collection_config)
        
        schema = {
            "fields": fields,
            "description": collection_config.get("description", ""),
            "create_indexes": collection_config.get("create_indexes", [])
        }
        
        return schema
    
    def _prepare_fields(self, collection_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process and prepare collection fields"""
        fields = []
        
        for field in collection_config.get("fields", []):
            field_copy = field.copy()
            
            if field_copy.get("name") == "embedding" and field_copy.get("dtype") == "FLOAT_VECTOR":
                field_copy["dim"] = self.embedding_dimension
                
            fields.append(field_copy)
        
        fields = self._ensure_required_fields(fields)
        
        return fields
    
    def _ensure_required_fields(self, fields: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ensure required fields exist in the schema"""
        if not any(field.get("name") == "id" for field in fields):
            fields.append({
                "name": "id",
                "dtype": "VARCHAR",
                "is_primary": True,
                "max_length": 100
            })
        
        if not any(field.get("name") == "embedding" and field.get("dtype") == "FLOAT_VECTOR" 
                  for field in fields):
            fields.append({
                "name": "embedding",
                "dtype": "FLOAT_VECTOR",
                "dim": self.embedding_dimension
            })
        
        return fields
        
    async def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """Get information about a collection"""
        try:
            collections = await self.vdb_client.list_collections()
            if collection_name not in collections:
                return {"status": "error", "message": "Collection not found"}
            
            return await self.vdb_client.get_collection_info(collection_name)
        except Exception as e:
            print(f"Error fetching collection info: {str(e)}")
            return {"status": "error", "message": str(e)}