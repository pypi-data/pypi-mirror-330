from contextlib import asynccontextmanager
import json
import os
from fastapi import BackgroundTasks, Depends, FastAPI, Response
import uvicorn
from gru.agents.checkpoint.task_results import TaskResultsRepository, TaskStatus
from gru.agents.framework_wrappers import AgentWorkflow
from gru.agents.schemas import AgentInvokeRequest, AgentInvokeResponse
from gru.agents.schemas.schemas import AgentConversationRequest, TaskCompleteRequest
import logging
from gru.agents.utils.logging import get_log_fields

from gru.agents.schemas.memory import (
    MemoryStoreRequest,
    MemoryRetrieveParams,
    MemoryUpdateRequest,
    MemoryDeleteRequest,
    MemoryResponse
)
from gru.agents.framework_wrappers.memory import CansoMemory

agent_name = os.getenv("AGENT_NAME")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):

    workflow: AgentWorkflow = app.state.workflow
    await workflow.setup()
    app.state.task_results_repo = TaskResultsRepository()
    await app.state.task_results_repo.setup()
    yield


api = FastAPI(lifespan=lifespan)

def get_memory() -> CansoMemory:
    return api.state.memory

async def invoke_workflow(request: AgentInvokeRequest):
    try:
        workflow: AgentWorkflow = api.state.workflow
        output = await workflow.invoke(request)
        # Todo: Save output to DB table
        print(output)
    except Exception as e:
        logger.error(
            f"AI agent: invoke api failed - {e}",
            extra=get_log_fields(correlation_id=request.prompt_id),
        )


async def resume_workflow(request: TaskCompleteRequest):
    try:
        workflow: AgentWorkflow = api.state.workflow
        output = await workflow.resume(request)
        # Todo: Save output to DB table
        print(output)
    except Exception as e:
        logger.error(
            f"AI agent: resume workflow failed: {e}",
            extra=get_log_fields(correlation_id=request.prompt_id),
        )


async def update_task_result(request: TaskCompleteRequest):
    try:
        task_results_repo: TaskResultsRepository = api.state.task_results_repo
        await task_results_repo.update(
            agent_name,
            request.prompt_id,
            request.task_type,
            request.tool_call_id,
            TaskStatus.COMPLETED,
            json.dumps(request.result),
        )
    except Exception as e:
        logger.error(
            f"AI agent: Error while upddating task result - {e}",
            extra=get_log_fields(correlation_id=request.prompt_id),
        )


@api.post("/invoke")
async def invoke(
    request: AgentInvokeRequest, background_tasks: BackgroundTasks
) -> AgentInvokeResponse:
    background_tasks.add_task(invoke_workflow, request)
    return AgentInvokeResponse(prompt_id=request.prompt_id)


@api.post("/converse")
async def converse(request: AgentConversationRequest):
    try:
        workflow: AgentWorkflow = api.state.workflow
        return await workflow.converse(request)
    except Exception as e:
        logger.error(
            f"AI agent converse api failed: {e}",
            extra=get_log_fields(correlation_id=request.conversation_id),
        )


@api.post("/task-complete")
async def task_complete(
    request: TaskCompleteRequest, background_tasks: BackgroundTasks
):
    background_tasks.add_task(resume_workflow, request)
    return Response(status_code=200)


@api.post("/save-task-result")
async def save_task_result(
    request: TaskCompleteRequest, background_tasks: BackgroundTasks
):
    background_tasks.add_task(update_task_result, request)
    return Response(status_code=200)


@api.post("/memory", response_model=MemoryResponse)
async def store_memory(request: MemoryStoreRequest, memory: CansoMemory = Depends(get_memory)
):

    result = await memory.store(
        data={
            "text": request.text,
            "metadata": request.metadata
        },
        collection_name=request.collection_name
    )

    return MemoryResponse(
        status=result.status,
        message=result.message,
        data={"memory_id": result.ids[0]}
    )

@api.get("/memory", response_model=MemoryResponse)
async def retrieve_memory(params: MemoryRetrieveParams = Depends(), memory: CansoMemory = Depends(get_memory)):
    try:
        results = await memory.retrieve(
            query=params.query,
            collection_name=params.collection_name,
            top_k=params.top_k or 5
        )

        return MemoryResponse(
            status="success",
            message="Retrieved matching documents",
            data={"results": results.results}
        )
    except Exception as e:
        print(f"Error in retrieve endpoint: {str(e)}")
        return MemoryResponse(
            status="error",
            message=f"Error retrieving documents: {str(e)}",
            data={"results": []}
        )

@api.patch("/memory", response_model=MemoryResponse)
async def update_memory(request: MemoryUpdateRequest, memory: CansoMemory = Depends(get_memory)):
    try:
        result = await memory.update(
            doc_id=request.doc_id,
            data={
                "text": request.text,
                "metadata": request.metadata
            },
            collection_name=request.collection_name
        )

        if result.get("status") == "error":
            return MemoryResponse(
                status="error",
                message=result.message,
                data={}
            )

        return MemoryResponse(
            status="success",
            message="Document updated successfully",
            data={"count": result.updated_count}
        )
    except Exception as e:
        return MemoryResponse(
            status="error",
            message=f"Error updating document: {str(e)}",
            data=None
        )

@api.delete("/memory", response_model=MemoryResponse)
async def delete_memory(request: MemoryDeleteRequest, memory: CansoMemory = Depends(get_memory)):

    result = await memory.delete(
        doc_id=request.doc_id,
        collection_name=request.collection_name
    )

    return MemoryResponse(
        status=result.status,
        message=result.message,
    )

@api.get("/memory/collections", response_model=MemoryResponse)
async def list_collections(memory: CansoMemory = Depends(get_memory)):
    collections = await memory.vdb_client.list_collections()
    
    return MemoryResponse(
        status=collections.status,
        message=collections.message,
        data={"collections": collections.collections}
    )

@api.get("/memory/collections/{collection_name}", response_model=MemoryResponse)
async def get_collection_info(collection_name: str, memory: CansoMemory = Depends(get_memory)):
        
    info = await memory.vdb_client.get_collection_info(collection_name)
    
    return MemoryResponse(
        status=info.status,
        message=info.message,
        data={"collection_info": info.collection_info}
    )


class App:


    def __init__(self, workflow: AgentWorkflow, memory: CansoMemory):

        api.state.workflow = workflow
        api.state.memory = memory

    def run(self):
        uvicorn.run(api, host="0.0.0.0", port=8080)
