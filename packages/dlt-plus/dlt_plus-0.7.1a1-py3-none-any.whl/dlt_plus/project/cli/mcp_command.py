import argparse

from dlt.common import logger
from dlt.cli import SupportsCliCommand
from dlt_plus.common.license import ensure_license_with_scope
from dlt_plus.common.license.license import DltLicenseException


class MCPCommand(SupportsCliCommand):
    command = "mcp"
    help_string = "Launch a dlt MCP server"
    description = (
        "The MCP server allows LLMs to interact with your dlt pipelines and your dlt+ projects."
    )

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        subparser = parser.add_subparsers(title="Available subcommands", dest="mcp_command")

        subparser.add_parser(
            "run", help="Launch dlt MCP server from current environment and working directory"
        )
        subparser.add_parser(
            "run_plus", help="Launch dlt+ MCP server from current environment and working directory"
        )

    def execute(self, args: argparse.Namespace) -> None:
        if args.mcp_command == "run":
            start_mcp()

        elif args.mcp_command == "run_plus":
            try:
                # TODO move the license check to inside the MCP at tool registration
                # this would allow the bare MCP to report a useful message through the IDE interface
                ensure_license_with_scope("*")
                start_mcp_plus()
            except DltLicenseException:
                start_mcp()


def start_mcp() -> None:
    from dlt_plus.mcp.server import DltMCP

    logger.info("Starting dlt MCP server")
    mcp_server = DltMCP(project_mode=False)
    mcp_server.run()


def start_mcp_plus() -> None:
    from dlt_plus.mcp.server import DltMCP

    logger.info("Starting dlt+ MCP server")
    mcp_server = DltMCP(project_mode=True)
    mcp_server.run()
