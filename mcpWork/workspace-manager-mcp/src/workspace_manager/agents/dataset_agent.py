from __future__ import annotations

from pathlib import Path
from typing import Any

from ..models import WorkspaceConfig
from ..security import SecurityGuard
from ..utils.logger import WorkspaceLogger


class DatasetAgent:
    """Create dataset folders for common ML tasks."""

    def __init__(self, config: WorkspaceConfig, security: SecurityGuard, logger: WorkspaceLogger) -> None:
        self.config = config
        self.security = security
        self.logger = logger

    def create_dataset(self, name: str, kind: str = "classification") -> dict[str, Any]:
        safe_name = self.security.validate_name(name)
        target = Path(self.config.resolve_workspace_root()) / safe_name
        target.mkdir(parents=True, exist_ok=True)

        folders = ["train/images", "train/labels", "val/images", "val/labels", "test/images", "test/labels"]
        for folder in folders:
            (target / folder).mkdir(parents=True, exist_ok=True)

        readme = target / "README.md"
        readme.write_text(f"# {safe_name}\n\nDataset kind: {kind}\n", encoding="utf-8")

        return {"success": True, "dataset": safe_name, "kind": kind, "folders": folders, "path": str(target)}
