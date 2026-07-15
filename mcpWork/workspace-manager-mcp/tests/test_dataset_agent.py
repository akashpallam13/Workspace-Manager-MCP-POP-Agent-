from pathlib import Path
from tempfile import TemporaryDirectory

from workspace_manager.agents.dataset_agent import DatasetAgent
from workspace_manager.models import WorkspaceConfig
from workspace_manager.security import SecurityGuard
from workspace_manager.utils.logger import WorkspaceLogger


def test_create_dataset_creates_folder_structure() -> None:
    with TemporaryDirectory() as tmp_dir:
        config = WorkspaceConfig(workspace_root=tmp_dir)
        agent = DatasetAgent(config, SecurityGuard(tmp_dir), WorkspaceLogger(level="INFO"))

        result = agent.create_dataset("cats", "classification")

        assert result["success"] is True
        assert (Path(tmp_dir) / "cats" / "train" / "images").exists()
        assert (Path(tmp_dir) / "cats" / "README.md").exists()
