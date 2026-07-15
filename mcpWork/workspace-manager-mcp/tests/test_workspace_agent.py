from pathlib import Path
from tempfile import TemporaryDirectory

from workspace_manager.agents.workspace_agent import WorkspaceAgent
from workspace_manager.models import WorkspaceConfig
from workspace_manager.security import SecurityGuard
from workspace_manager.utils.logger import WorkspaceLogger


def test_create_project_and_file() -> None:
    with TemporaryDirectory() as tmp_dir:
        config = WorkspaceConfig(workspace_root=str(Path(tmp_dir) / "workspace"))
        security = SecurityGuard(config.resolve_workspace_root())
        logger = WorkspaceLogger(level="INFO")
        agent = WorkspaceAgent(config, security, logger)

        result = agent.create_project("demo")
        assert result["success"] is True
        assert (config.resolve_workspace_root() / "demo").exists()

        file_result = agent.create_file("demo/README.md", "hello")
        assert file_result["success"] is True
        assert (config.resolve_workspace_root() / "demo/README.md").exists()

        read_result = agent.read_file("demo/README.md")
        assert read_result["content"] == "hello"
