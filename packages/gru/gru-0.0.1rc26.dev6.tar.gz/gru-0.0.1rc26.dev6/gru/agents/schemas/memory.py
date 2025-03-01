from typing import Any, Dict, Optional
from pydantic import BaseModel

class MemoryStoreRequest(BaseModel):
    collection_name: str
    text: str
    metadata: Optional[Dict[str, Any]] = None

class MemoryRetrieveParams(BaseModel):
    collection_name: str
    query: str
    top_k: Optional[int] = 5

class MemoryUpdateRequest(BaseModel):
    collection_name: str
    doc_id: str
    text: str
    metadata: Optional[Dict[str, Any]] = None

class MemoryDeleteRequest(BaseModel):
    collection_name: str
    doc_id: str

class MemoryListCollectionsRequest(BaseModel):
    pass

class MemoryGetCollectionInfoRequest(BaseModel):
    collection_name: str

class MemoryResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None