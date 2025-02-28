from typing import Optional, Type
from github import Github, Auth
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_core.callbacks import CallbackManagerForToolRun


class GitRepoContentToolInput(BaseModel):
    repository: str = Field(
        description="repository of which the contents are to be retrieved"
    )


class GitRepoContentRetriever(BaseTool):
    name: str = "get_git_repo_contents"
    description: str = (
        "Use this to get file paths of all the files in a github repository"
    )
    args_schema: Type[BaseModel] = GitRepoContentToolInput
    return_direct: bool = True

    class Config:
        extra = "allow"

    def __init__(self, token: str):
        super().__init__(token=token)
        self.token = token

    def _run(self, *args, **kwargs):
        return super()._run(*args, **kwargs)

    async def _arun(
        self,
        repository: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        auth = Auth.Token(self.token)
        g = Github(auth=auth)
        repo = g.get_repo(repository)

        contents = repo.get_contents("")

        result = []
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                result.append(file_content.path)

        return result
