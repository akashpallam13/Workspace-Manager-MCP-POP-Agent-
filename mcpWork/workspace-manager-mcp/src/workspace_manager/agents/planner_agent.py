from __future__ import annotations

from typing import Any

from ..models import WorkspaceConfig
from ..security import SecurityGuard
from ..utils.logger import WorkspaceLogger


class PlannerAgent:
    """Map a natural-language intent to concrete workspace operations."""

    def __init__(self, config: WorkspaceConfig, security: SecurityGuard, logger: WorkspaceLogger) -> None:
        self.config = config
        self.security = security
        self.logger = logger

    def handle(self, prompt: str) -> dict[str, Any]:
        lowered = prompt.lower()
        if "react" in lowered:
            return {"success": True, "plan": ["create_project:react-app", "create_folder:src", "create_folder:public", "create_file:README.md"]}
        if "yolo" in lowered:
            return {"success": True, "plan": ["create_project:yolo-project", "create_folder:train/images", "create_folder:train/labels", "create_file:requirements.txt"]}
        if "fastapi" in lowered:
            return {"success": True, "plan": ["create_project:fastapi-app", "create_file:main.py", "create_file:requirements.txt", "create_file:README.md"]}
        return {"success": True, "plan": ["create_project:workspace-project"]}
