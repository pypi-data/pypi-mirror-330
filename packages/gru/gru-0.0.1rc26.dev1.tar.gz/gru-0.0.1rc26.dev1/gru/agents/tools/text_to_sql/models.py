from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class TextToSQLToolInput(BaseModel):
    query: str = Field(description="Natural language query to convert to SQL")
    table_info: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Optional table information to initialize or update the context",
    )
