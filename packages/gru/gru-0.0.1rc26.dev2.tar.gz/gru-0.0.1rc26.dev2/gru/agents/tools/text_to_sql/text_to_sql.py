from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from gru.agents.tools.core.services.text_to_sql import TextToSQLService
from gru.agents.tools.text_to_sql.models import TextToSQLToolInput


class TextToSQLTool(BaseTool):
    name: str = "text_to_sql_converter"
    description: str = "Use this tool to convert natural language queries into SQL."
    args_schema: Type[BaseModel] = TextToSQLToolInput
    return_direct: bool = True

    class Config:
        extra = "allow"

    def __init__(self, service: TextToSQLService):
        super().__init__()
        self.service = service

    def _run(self, *args, **kwargs):
        return super()._run(*args, **kwargs)

    async def _arun(
        self,
        query: str,
        table_info: Optional[List[Dict[str, Any]]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        try:
            sql = await self.service.convert_to_sql(query=query, table_info=table_info)
            return sql
        except Exception as e:
            if run_manager:
                run_manager.on_tool_error(e)
            return f"Error converting text to SQL: {str(e)}"
