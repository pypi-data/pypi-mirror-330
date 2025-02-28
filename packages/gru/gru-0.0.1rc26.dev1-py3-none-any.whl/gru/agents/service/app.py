from contextlib import asynccontextmanager
import json
import os
from fastapi import BackgroundTasks, FastAPI, Response
import uvicorn
from gru.agents.checkpoint.task_results import TaskResultsRepository, TaskStatus
from gru.agents.framework_wrappers import AgentWorkflow
from gru.agents.schemas import AgentInvokeRequest, AgentInvokeResponse
from gru.agents.schemas.schemas import AgentConversationRequest, TaskCompleteRequest
import logging
from gru.agents.utils.logging import get_log_fields

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


class App:
    def __init__(self, workflow: AgentWorkflow):
        api.state.workflow = workflow

    def run(self):
        uvicorn.run(api, host="0.0.0.0", port=8080)
