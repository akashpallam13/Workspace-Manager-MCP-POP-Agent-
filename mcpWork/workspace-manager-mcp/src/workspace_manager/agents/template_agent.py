from __future__ import annotations

from typing import Any

from ..models import WorkspaceConfig
from ..security import SecurityGuard
from ..utils.logger import WorkspaceLogger


class TemplateAgent:
    """Generate starter project structures for common templates."""

    def __init__(self, config: WorkspaceConfig, security: SecurityGuard, logger: WorkspaceLogger) -> None:
        self.config = config
        self.security = security
        self.logger = logger

    def generate(self, template_name: str) -> dict[str, Any]:
        files = {
            "python": ["README.md", "main.py", "requirements.txt"],
            "react": ["README.md", "package.json", "src/App.jsx"],
            "fastapi": ["README.md", "main.py", "requirements.txt"],
            "ai": ["README.md", "notebooks/intro.ipynb", "requirements.txt"],
            "yolo": ["README.md", "requirements.txt", "train/images", "train/labels"],
            "research": ["README.md", "notes.md", "data/"],
            "documentation": ["README.md", "CHANGELOG.md", "architecture.md"],
            "data-science": ["README.md", "requirements.txt", "notebooks/analysis.ipynb"],
        }
        return {"success": True, "template": template_name, "files": files.get(template_name, ["README.md"])}
