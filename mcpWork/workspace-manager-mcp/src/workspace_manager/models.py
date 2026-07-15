from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class WorkspaceConfig(BaseModel):
    """Configuration for the workspace manager."""

    workspace_root: str = "workspace"
    max_file_size_mb: int = 50
    allowed_extensions: list[str] = Field(default_factory=lambda: [".py", ".md", ".json", ".csv", ".txt", ".toml", ".zip"])
    log_level: str = "INFO"
    template_dir: str = "templates"

    def resolve_workspace_root(self) -> Path:
        return Path(self.workspace_root).resolve()
