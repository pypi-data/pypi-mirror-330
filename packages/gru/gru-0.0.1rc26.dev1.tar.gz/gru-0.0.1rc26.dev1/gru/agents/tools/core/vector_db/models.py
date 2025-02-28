from pydantic import BaseModel


class VectorDBConfig(BaseModel):
    host: str
    port: int
    index_type: str
    dim: int
    metric: str = "cosine"
    nprobe: int = 6
