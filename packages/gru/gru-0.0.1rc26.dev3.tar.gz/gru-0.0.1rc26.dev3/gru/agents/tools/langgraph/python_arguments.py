import ast
from typing import Optional, Type
from github import Github, Auth
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_core.callbacks import CallbackManagerForToolRun


class PythonArgumentsToolInput(BaseModel):
    repository: str = Field(description="repository containing the python file")
    file_path: str = Field(description="path of the python file in the repository")


class PythonArgumentsTool(BaseTool):
    name: str = "get_python_file_arguments"
    description: str = (
        "Use this to determine the command line arguments that are required to execute a python file present in a repository"
    )
    args_schema: Type[BaseModel] = PythonArgumentsToolInput
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
        file_path: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        auth = Auth.Token(self.token)
        g = Github(auth=auth)
        repo = g.get_repo(repository)

        contents = repo.get_contents(file_path)
        source = contents.decoded_content.decode()

        arg_details = self.analyze_cmdline_args(source)

        return arg_details

    def analyze_cmdline_args(self, source: str):

        tree = ast.parse(source)

        argparse_details = []

        class ArgumentVisitor(ast.NodeVisitor):

            def is_argparse_constructor(self, node):
                return (
                    isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "argparse"
                    and node.func.attr == "ArgumentParser"
                )

            def extract_argument_values(self, node):
                return [arg.value for arg in node.args if isinstance(arg, ast.Constant)]

            def collect_add_arguments(self, tree):
                for parent in ast.walk(tree):
                    if (
                        isinstance(parent, ast.Call)
                        and isinstance(parent.func, ast.Attribute)
                        and parent.func.attr == "add_argument"
                    ):
                        args = self.extract_argument_values(parent)
                        if args:
                            argparse_details.extend(args)

            def visit_Call(self, node):
                if self.is_argparse_constructor(node):
                    self.collect_add_arguments(tree)

        visitor = ArgumentVisitor()
        visitor.visit(tree)

        return argparse_details
