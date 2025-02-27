import os
from typing import Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Prompt

from dlt_plus.project.run_context import ProjectRunContext
from dlt_plus.mcp import tools
from dlt_plus.mcp import prompts


class DltMCP(FastMCP):
    def __init__(self, project_mode: bool = False) -> None:
        super().__init__(
            name="dlt+",
            dependencies=["dlt-plus", "dlt"],
        )
        self._project_context: Optional[ProjectRunContext] = None
        self.project_mode = project_mode

        # TODO use conditional registration when dynamic tool is better supported by clients
        # if mcp_server.project_context is None:
        #     mcp_server.add_tool(tools.project.select_or_create_dlt_project)
        # else:
        #     for tool in tools.project.__tools__:
        #         mcp_server.add_tool(tool)
        if self.project_mode is True:
            self.add_tool(tools.project.select_or_create_dlt_project)
            for tool in tools.project.__tools__:
                self.add_tool(tool)
            for prompt_fn in prompts.project.__prompts__:
                self.add_prompt(Prompt.from_function(prompt_fn))
        else:
            for tool in tools.pipeline.__tools__:  # type: ignore[assignment]
                self.add_tool(tool)
            for prompt_fn in prompts.pipeline.__prompts__:
                self.add_prompt(Prompt.from_function(prompt_fn))

    @property
    def project_context(self) -> Optional[ProjectRunContext]:
        return self._project_context

    @project_context.setter
    def project_context(self, value: ProjectRunContext) -> None:
        self._project_context = value
        # setting the working directory should become part of the Python SDk
        # it's already in the Typescript SDK
        # ref: https://github.com/modelcontextprotocol/typescript-sdk/pull/146
        os.chdir(value.run_dir)


if __name__ == "__main__":
    mcp_server = DltMCP(project_mode=False)
    mcp_server.run()
