from typing import Any, Dict, List, Optional
import os, json, uuid, traceback
from datetime import datetime
from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    connections,
    utility
)
from gru.agents.tools.core.vector_db.base import (
    AddToCollectionResponse, 
    CreateCollectionResponse, 
    DeleteFromCollectionResponse,
    DropCollectionResponse,
    GetCollectionInfoResponse,
    ListCollectionsResponse, 
    SimilaritySearchResponse, 
    UpdateCollectionResponse, 
    VectorDBClient, 
    VectorDBConfig
)
from pymilvus.exceptions import DataNotMatchException


class MilvusClient(VectorDBClient):
    MILVUS_TYPES = {
        "INT64": DataType.INT64,
        "VARCHAR": DataType.VARCHAR,
        "FLOAT_VECTOR": DataType.FLOAT_VECTOR,
        "FLOAT": DataType.FLOAT,
        "BOOL": DataType.BOOL
    }

    DEFAULT_INDEX_PARAMS = {
        DataType.FLOAT_VECTOR: {
            "index_type": "IVF_FLAT",
            "params": {
                "nlist": 1024,
                "metric_type": "L2"
            }
        },
        DataType.VARCHAR: {
            "index_type": "Trie",
            "params": {}
        },
        DataType.INT64: {
            "index_type": "STL_SORT",
            "params": {}
        },
        DataType.FLOAT: {
            "index_type": "STL_SORT",
            "params": {}
        }
    }

    def __init__(self):
        self.config = VectorDBConfig(
            host=os.getenv("MILVUS_HOST", "localhost"),
            port=int(os.getenv("MILVUS_PORT", "19530")),
            user=os.getenv("MILVUS_USER", "root"),
            password=os.getenv("MILVUS_PASSWORD", "Milvus"),
            connection_timeout=int(os.getenv("MILVUS_CONNECTION_TIMEOUT", "30")),
            max_retries=int(os.getenv("MILVUS_MAX_RETRIES", "3"))
        )
        self.connect(self.config)

    def connect(self, config:VectorDBConfig) -> None:
        """Initialize connection to Milvus"""
        try:
            connections.connect(
                alias="default",
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
                timeout=config.connection_timeout
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Milvus: {str(e)}")

    def _create_field_schema(self, field_config: Dict[str, Any]) -> FieldSchema:
        return FieldSchema(
            name=field_config["name"],
            dtype=self.MILVUS_TYPES[field_config["dtype"]],
            is_primary=field_config.get("is_primary", False),
            auto_id=field_config.get("auto_id", False),
            max_length=field_config.get("max_length"),
            dim=field_config.get("dim")
        )

    def create_collection_sync(
            self,
            collection_name: str,
            schema: Dict[str, Any],
            replace_existing: bool = False
    ) -> CreateCollectionResponse:
        """Create a new collection with specified schema synchronously"""
        try:
            if utility.has_collection(collection_name):
                if replace_existing:
                    print(f"Dropping existing collection: {collection_name}")
                    utility.drop_collection(collection_name)
                else:
                    return CreateCollectionResponse(
                        status="error",
                        message=f"Collection {collection_name} already exists",
                        collection_name=collection_name
                    )

            field_schemas = []
            for field in schema["fields"]:
                if field["dtype"] == "FLOAT_VECTOR":
                    if "dim" not in field:
                        return CreateCollectionResponse(
                            status="error",
                            message=f"Dimension required for FLOAT_VECTOR field {field['name']}",
                            collection_name=collection_name
                        )
                    field_schema = FieldSchema(
                        name=field["name"],
                        dtype=self.MILVUS_TYPES[field["dtype"]],
                        dim=field["dim"],
                        is_primary=field.get("is_primary", False),
                        auto_id=field.get("auto_id", False)
                    )
                else:
                    field_schema = FieldSchema(
                        name=field["name"],
                        dtype=self.MILVUS_TYPES[field["dtype"]],
                        is_primary=field.get("is_primary", False),
                        auto_id=field.get("auto_id", False),
                        max_length=field.get("max_length")
                    )
                field_schemas.append(field_schema)

            collection_schema = CollectionSchema(
                fields=field_schemas,
                description=schema.get("description", "")
            )

            collection = Collection(
                name=collection_name,
                schema=collection_schema
            )

            explicit_indexes = schema.get("create_indexes", [])
            if explicit_indexes:
                print(f"Creating explicitly defined indexes for collection {collection_name}")
                
                for index_def in explicit_indexes:
                    field_name = index_def.get("field_name")
                    index_params = index_def.get("index_params", {})
                    
                    if not field_name:
                        print("Skipping index with no field_name specified")
                        continue
                        
                    print(f"Creating index for field {field_name}")
                    collection.create_index(
                        field_name=field_name,
                        index_params=index_params
                    )
            collection.load()
            return CreateCollectionResponse(
                status="success",
                message=f"Collection {collection_name} created successfully",
                collection_name=collection_name
            )
        except Exception as e:
            return CreateCollectionResponse(
                status="error",
                message=f"Failed to create collection: {str(e)}",
                collection_name=collection_name
            )

    async def create_collection(
        self,
        collection_name: str,
        schema: Dict[str, Any],
        replace_existing: bool = False
    ) -> CreateCollectionResponse:
        try:
            if utility.has_collection(collection_name):
                if replace_existing:
                    utility.drop_collection(collection_name)
                else:
                    return CreateCollectionResponse(
                        status="error",
                        message=f"Collection {collection_name} already exists",
                        collection_name=collection_name
                    )

            field_schemas = [
                self._create_field_schema(field) 
                for field in schema["fields"]
            ]
            collection_schema = CollectionSchema(
                fields=field_schemas,
                description=schema.get("description", "")
            )
            
            collection = Collection(
                name=collection_name, 
                schema=collection_schema
            )

            # Create indexes for each field based on its type
            for field_schema in field_schemas:
                index_params = self.DEFAULT_INDEX_PARAMS.get(field_schema.dtype)
                if index_params:
                    collection.create_index(
                        field_name=field_schema.name,
                        index_params=index_params
                    )
            collection.load()
            return CreateCollectionResponse(
                status="success",
                message=f"Collection {collection_name} created successfully",
                collection_name=collection_name
            )
        except Exception as e:
            return CreateCollectionResponse(
                status="error",
                message=f"Failed to create collection: {str(e)}",
                collection_name=collection_name
            )

    async def add_to_collection(
        self, 
        collection_name: str,
        embeddings: List[List[float]],
        data: List[Dict[str, Any]]
    ) -> AddToCollectionResponse:
        try:
            collection = Collection(collection_name)
            schema = collection.schema
            field_names = {field.name for field in schema.fields}  

            data_to_insert = []
            for embedding, meta in zip(embeddings, data):
                doc = {
                    "id": meta.get("id", str(uuid.uuid4())),
                    "embedding": embedding
                }

                for field_name in field_names:
                    if field_name == "id" or field_name == "embedding":
                        continue  

                    if field_name in meta:
                        value = meta.get(field_name)
                        doc[field_name] = json.dumps(value) if isinstance(value, dict) else value

                if "created_at" not in doc:
                    doc["created_at"] = datetime.utcnow().isoformat()

                data_to_insert.append(doc)

            print(f"Inserting {len(data_to_insert)} documents into {collection_name}")
            result = collection.insert(data_to_insert)

            return AddToCollectionResponse(
                status="success",
                message=f"Inserted {len(data_to_insert)} documents into {collection_name}",
                ids=result.primary_keys
            )
        except DataNotMatchException as e:
            return AddToCollectionResponse(
                status="error",
                message=f"Data does not match schema: {str(e)}",
                ids=[]
            )
        except Exception as e:
            print(f"Error in add_to_collection: {str(e)}")
            traceback.print_exc()
            return AddToCollectionResponse(
                status="error",
                message=f"Failed to insert data: {str(e)}",
                ids=[]
            )

    async def update_collection(
            self,
            collection_name: str,
            memory_id: str,
            embedding: List[float],
            metadata: Optional[Dict[str, Any]] = None
    ) -> UpdateCollectionResponse:
        try:
            collection = Collection(collection_name)

            # Get the schema to ensure consistent field handling
            schema = collection.schema
            field_names = {field.name for field in schema.fields}

            # First verify the document exists
            search_expr = f'id == "{memory_id}"'
            result = collection.query(
                expr=search_expr,
                output_fields=["id"]
            )

            if not result:
                return UpdateCollectionResponse(
                    status="error",
                    message=f"Document with id {memory_id} not found",
                    id=memory_id,
                    updated_count=0
                )

            # Delete existing document
            collection.delete(f"id == '{memory_id}'")

            # Construct new document with schema-aware fields
            doc = {
                "id": memory_id,
                "embedding": embedding,
                "text": metadata.get("text", ""),
                "created_at": metadata.get("created_at", datetime.now().isoformat())
            }

            # Handle metadata field if it exists in schema
            if "metadata" in field_names and metadata:
                meta_dict = metadata.get("metadata", {})
                doc["metadata"] = json.dumps(meta_dict)

                # Add any additional fields from metadata that match schema
                for field in schema.fields:
                    field_name = field.name
                    if field_name not in doc and field_name in meta_dict:
                        doc[field_name] = meta_dict[field_name]

            # Insert updated document
            insert_result = collection.insert([doc])

            return UpdateCollectionResponse(
                status="success",
                message="Document updated successfully",
                id=memory_id,
                updated_count=insert_result.insert_count
            )

        except Exception as e:
            return UpdateCollectionResponse(
                status="error",
                message=f"Failed to update document: {str(e)}",
                id=memory_id,
                updated_count=0
            )

    async def delete_from_collection(
        self,
        collection_name: str,
        memory_id: str
    ) -> DeleteFromCollectionResponse:
        try:
            collection = Collection(collection_name)
            delete_expr = f"id == '{memory_id}'"
            result = collection.delete(delete_expr)
            
            return DeleteFromCollectionResponse(
                status="success",
                message=f"Deleted {result.delete_count} documents from {collection_name}",
            )
        except Exception as e:
            return DeleteFromCollectionResponse(
                status="error",
                message=f"Failed to delete document: {str(e)}"
            )
        
    async def similarity_search(
        self,
        collection_name: str,
        query_vector: List[float],
        anns_field: Optional[str] = None,
        top_k: int = 5,
        search_params: Optional[Dict[str, Any]] = None,
        output_fields: Optional[List[str]] = None,
    ) -> SimilaritySearchResponse:
        """
        Performs a similarity search using the query vector
        and returns top-k results.
        """
        collection = Collection(collection_name)

        # If anns_field is not provided, use the first float vector field
        if anns_field is None:
            schema = collection.schema
            for field in schema.fields:
                if field.dtype == DataType.FLOAT_VECTOR:
                    anns_field = field.name
                break  
        
        # If output_fields is not provided, use all fields except anns_field
        if output_fields is None:
            schema = collection.schema
            output_fields = [field.name for field in schema.fields 
                            if field.dtype != DataType.FLOAT_VECTOR]

        if search_params is None:
            search_params = {
                "metric_type":  "L2",
                "params": {
                    "nprobe": 10
                },
            }

        # Perform the search
        try:
            results = collection.search(
            data=[query_vector], 
            anns_field=anns_field,
            param=search_params,
            limit=top_k,
            output_fields=output_fields,
        )
        except Exception as e:
            print(f"Error in similarity_search: {str(e)}")
            return SimilaritySearchResponse(
                status="error",
                message=f"Failed to search: {str(e)}",
                results=[]
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

        return SimilaritySearchResponse(
            status="success",
            message="Search completed successfully",
            results=search_results
        )

    async def filtered_search(
        self,
        collection_name: str,
        filter_expr: str,
        limit: int = 5,
        output_fields: Optional[List[str]] = None,
    ) -> SimilaritySearchResponse:
        """Performs a filtered search based on additional query parameters."""
        collection = Collection(collection_name)

        results = collection.query(
            expr=filter_expr, output_fields=output_fields, limit=limit
        )

        return SimilaritySearchResponse(
            status="success",
            message="Search completed successfully",
            results=results
        )

    async def list_collections(self) -> ListCollectionsResponse:
        try:
            print("Inside milvus client")
            return ListCollectionsResponse(
                status="success",
                message="Collections listed successfully",
                collections=utility.list_collections()
            )
        except Exception as e:
            print(f"Failed to list collections: {str(e)}")
            return ListCollectionsResponse(
                status="error",
                message=f"Failed to list collections: {str(e)}",
                collections=[]
            )
    
    # TODO reuse in Canso_memory
    async def get_collection_info(
        self,
        collection_name: str
    ) -> GetCollectionInfoResponse:
        """Get collection metadata and statistics"""
        try:
            if not utility.has_collection(collection_name):
                return GetCollectionInfoResponse(
                    status="error",
                    message=f"Collection {collection_name} does not exist",
                    collection_info={}
                )
                
            collection = Collection(collection_name)
            
            fields_info = []
            for field in collection.schema.fields:
                field_info = {
                    "name": field.name,
                    "dtype": str(field.dtype),
                    "is_primary": field.is_primary
                }
                if hasattr(field, "dim") and field.dim is not None:
                    field_info["dim"] = field.dim
                if hasattr(field, "max_length") and field.max_length is not None:
                    field_info["max_length"] = field.max_length
                    
                fields_info.append(field_info)
            
            index_info = []
            for index in collection.indexes:
                index_info.append({
                    "field_name": index.field_name,
                    "index_type": index.params.get("index_type", ""),
                    "params": index.params.get("params", {})
                })
            
            return GetCollectionInfoResponse(
                status="success",
                message="Collection info retrieved successfully",
                collection_info={
                    "name": collection_name,
                    "entity_count": collection.num_entities,
                    "fields": fields_info,
                    "indexes": index_info,
                    "description": collection.schema.description
                }
            )
        except Exception as e:
            print(f"Error in get_collection_info: {str(e)}")
            traceback.print_exc()
            return GetCollectionInfoResponse(
                status="error",
                message=f"Failed to get collection info: {str(e)}",
                collection_info={}
            )

    async def drop_collection(
        self,
        collection_name: str
    ) -> DropCollectionResponse:
        try:
            utility.drop_collection(collection_name)
            return DropCollectionResponse(
                status="success",
                message=f"Collection {collection_name} dropped successfully"
            )
        except Exception as e:
            return DropCollectionResponse(
                status="error",
                message=f"Failed to drop collection: {str(e)}"
            )
