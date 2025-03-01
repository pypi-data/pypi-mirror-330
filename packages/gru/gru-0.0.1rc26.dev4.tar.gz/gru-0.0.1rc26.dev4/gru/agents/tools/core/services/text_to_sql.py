from gru.agents.tools.core.code_generator.sql import SQLCodeGenerator
from gru.agents.tools.core.query_analyzer.nl_query import NLQueryAnalyzer
from gru.agents.tools.core.code_generator.models import QueryIntent, RetrievalResult
from gru.agents.tools.core.llm_client.base import LLMClient
from gru.agents.tools.core.context_retriever.base import ContextRetriever
from gru.agents.prompts.text_to_sql import (
    QUERY_ANALYZER_USER_PROMPT_TEMPLATE,
    QUERY_ANALYZER_SYSTEM_PROMPT,
)
from typing import Optional, List, Dict, Any


class TextToSQLService:
    def __init__(
        self,
        llm_client: LLMClient,
        context_retriever: ContextRetriever,
        code_generator: Optional[SQLCodeGenerator] = None,
        query_analyzer: Optional[NLQueryAnalyzer] = None,
        system_prompt: Optional[str] = None,
        user_prompt_template: Optional[str] = None,
    ):
        self.llm_client = llm_client
        self.context_retriever = context_retriever
        self.code_generator = code_generator or SQLCodeGenerator(llm_client)
        self.query_analyzer = query_analyzer
        self.system_prompt = system_prompt or QUERY_ANALYZER_SYSTEM_PROMPT
        self.user_prompt_template = user_prompt_template or QUERY_ANALYZER_USER_PROMPT_TEMPLATE


    async def convert_to_sql(
        self, query: str, table_info: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        try:
            if table_info:
                await self.context_retriever.initialize_store(table_info)

            intent = await self._analyze_query(query)
            context = await self.context_retriever.retrieve_context(query, top_k=5)
            sql = await self._generate_sql(query, intent, context)
            await self.context_retriever.store_conversation(query, sql)

            return sql
        except Exception as e:
            return f"Error converting text to SQL: {str(e)}"
            

    async def _analyze_query(self, query: str) -> QueryIntent:
        user_prompt = self.user_prompt_template.format(query=query)
        response = await self.llm_client.generate(
            self.system_prompt, user_prompt
        )

        lines = response.split("\n")
        entities = lines[0].replace("Entities:", "").strip().strip("[]").split(",")
        domains = lines[1].replace("Domains:", "").strip().strip("[]").split(",")

        return QueryIntent(
            entities=[e.strip() for e in entities if e.strip()],
            domains=[d.strip() for d in domains if d.strip()],
        )

    async def _generate_sql(
        self, query: str, intent: QueryIntent, context: RetrievalResult
    ) -> str:
        return await self.code_generator.generate_code(query, intent, context)
