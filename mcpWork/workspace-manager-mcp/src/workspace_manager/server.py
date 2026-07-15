from __future__ import annotations

try:
    from fastmcp import FastMCP
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    class FastMCP:  # type: ignore[no-redef]
        def __init__(self, name: str) -> None:
            self.name = name

        def tool(self):
            def decorator(func):
                return func
            return decorator

        def run(self) -> None:
            print("FastMCP is not installed; server not started")

from .config import ConfigLoader
from .models import WorkspaceConfig
from .security import SecurityGuard
from .utils.logger import WorkspaceLogger
from .agents.planner_agent import PlannerAgent
from .agents.workspace_agent import WorkspaceAgent
from .agents.template_agent import TemplateAgent
from .agents.dataset_agent import DatasetAgent
from .agents.documentation_agent import DocumentationAgent
from .tools.project_tools import ProjectTools
from .tools.folder_tools import FolderTools
from .tools.file_tools import FileTools
from .tools.json_tools import JsonTools
from .tools.csv_tools import CsvTools
from .tools.search_tools import SearchTools
from .tools.zip_tools import ZipTools


class WorkspaceManagerServer:
    """Main MCP server application."""

    def __init__(self, config: WorkspaceConfig | None = None) -> None:
        self.config = config or ConfigLoader().load()
        self.logger = WorkspaceLogger(level=self.config.log_level)
        self.security = SecurityGuard(self.config.resolve_workspace_root())
        self.planner_agent = PlannerAgent(self.config, self.security, self.logger)
        self.workspace_agent = WorkspaceAgent(self.config, self.security, self.logger)
        self.template_agent = TemplateAgent(self.config, self.security, self.logger)
        self.dataset_agent = DatasetAgent(self.config, self.security, self.logger)
        self.documentation_agent = DocumentationAgent(self.config, self.security, self.logger)
        self.project_tools = ProjectTools(self.config.resolve_workspace_root())
        self.folder_tools = FolderTools(self.config.resolve_workspace_root())
        self.file_tools = FileTools(self.config.resolve_workspace_root())
        self.json_tools = JsonTools(self.config.resolve_workspace_root())
        self.csv_tools = CsvTools(self.config.resolve_workspace_root())
        self.search_tools = SearchTools(self.config.resolve_workspace_root())
        self.zip_tools = ZipTools(self.config.resolve_workspace_root())
        self.mcp = FastMCP("workspace-manager-mcp")
        self._register_tools()

    def _register_tools(self) -> None:
        @self.mcp.tool()
        def create_project(name: str) -> dict[str, object]:
            return self.workspace_agent.create_project(name)

        @self.mcp.tool()
        def list_projects() -> dict[str, object]:
            return self.workspace_agent.list_projects()

        @self.mcp.tool()
        def create_folder(path: str) -> dict[str, object]:
            return self.workspace_agent.create_folder(path)

        @self.mcp.tool()
        def create_file(path: str, content: str = "") -> dict[str, object]:
            return self.workspace_agent.create_file(path, content)

        @self.mcp.tool()
        def read_file(path: str) -> dict[str, object]:
            return self.workspace_agent.read_file(path)

        @self.mcp.tool()
        def write_file(path: str, content: str) -> dict[str, object]:
            return self.workspace_agent.write_file(path, content)

        @self.mcp.tool()
        def append_file(path: str, content: str) -> dict[str, object]:
            return self.file_tools.append_file(path, content)

        @self.mcp.tool()
        def delete_file(path: str) -> dict[str, object]:
            return self.file_tools.delete_file(path)

        @self.mcp.tool()
        def copy_file(source: str, destination: str) -> dict[str, object]:
            return self.file_tools.copy_file(source, destination)

        @self.mcp.tool()
        def compress_folder(folder: str = ".") -> dict[str, object]:
            return self.zip_tools.compress_folder(folder)

        @self.mcp.tool()
        def extract_zip(archive_path: str, destination: str | None = None) -> dict[str, object]:
            return self.zip_tools.extract_zip(archive_path, destination)

        @self.mcp.tool()
        def create_dataset(name: str, kind: str = "classification") -> dict[str, object]:
            return self.dataset_agent.create_dataset(name, kind)

        @self.mcp.tool()
        def read_json(path: str) -> dict[str, object]:
            return self.json_tools.read_json(path)

        @self.mcp.tool()
        def write_json(path: str, payload: dict[str, object]) -> dict[str, object]:
            return self.json_tools.write_json(path, payload)

        @self.mcp.tool()
        def update_json(path: str, updates: dict[str, object]) -> dict[str, object]:
            return self.json_tools.update_json(path, updates)

        @self.mcp.tool()
        def create_csv(path: str, rows: list[dict[str, object]]) -> dict[str, object]:
            return self.csv_tools.create_csv(path, rows)

        @self.mcp.tool()
        def append_csv(path: str, rows: list[dict[str, object]]) -> dict[str, object]:
            return self.csv_tools.append_csv(path, rows)

        @self.mcp.tool()
        def read_csv(path: str) -> dict[str, object]:
            return self.csv_tools.read_csv(path)

        @self.mcp.tool()
        def find_files(pattern: str) -> dict[str, object]:
            return self.search_tools.find_files(pattern)

        @self.mcp.tool()
        def search_content(term: str) -> dict[str, object]:
            return self.search_tools.search_content(term)

        @self.mcp.tool()
        def plan_request(prompt: str) -> dict[str, object]:
            return self.planner_agent.handle(prompt)

    def run(self) -> None:
        self.mcp.run()


def create_server() -> WorkspaceManagerServer:
    return WorkspaceManagerServer()


if __name__ == "__main__":
    create_server().run()
