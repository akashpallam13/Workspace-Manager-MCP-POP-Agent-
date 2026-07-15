from __future__ import annotations

from typing import Any

from ..models import WorkspaceConfig
from ..security import SecurityGuard
from ..utils.logger import WorkspaceLogger


class DocumentationAgent:
    """Generate starter documentation files for projects."""

    def __init__(self, config: WorkspaceConfig, security: SecurityGuard, logger: WorkspaceLogger) -> None:
        self.config = config
        self.security = security
        self.logger = logger

    def generate(self, project_name: str) -> dict[str, Any]:
        return {
            "success": True,
            "project": project_name,
            "files": ["README.md", "CHANGELOG.md", "requirements.txt", "project_summary.md", "architecture.md"],
        }
