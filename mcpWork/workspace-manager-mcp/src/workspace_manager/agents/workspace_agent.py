from __future__ import annotations

from pathlib import Path
from typing import Any

from ..exceptions import AlreadyExistsError, NotFoundError, WorkspaceError
from ..models import WorkspaceConfig
from ..security import SecurityGuard
from ..utils.logger import WorkspaceLogger
from ..utils.paths import WorkspacePathResolver


class WorkspaceAgent:
    """Manage projects, folders, and files within the secure workspace."""

    def __init__(self, config: WorkspaceConfig, security: SecurityGuard, logger: WorkspaceLogger) -> None:
        self.config = config
        self.security = security
        self.logger = logger
        self.resolver = WorkspacePathResolver(self.config.resolve_workspace_root())

    def create_project(self, name: str) -> dict[str, Any]:
        safe_name = self.security.validate_name(name)
        target = self.resolver.ensure_within_workspace(safe_name)
        try:
            target.mkdir(parents=True, exist_ok=False)
        except FileExistsError as exc:
            raise AlreadyExistsError(f"Project '{name}' already exists") from exc
        self.logger.info("Created project", project=name, path=str(target))
        return {"success": True, "message": "Project created.", "project": name, "path": str(target)}

    def list_projects(self) -> dict[str, Any]:
        root = self.config.resolve_workspace_root()
        projects = [p.name for p in root.iterdir() if p.is_dir()]
        return {"success": True, "projects": projects}

    def create_folder(self, path: str) -> dict[str, Any]:
        target = self.resolver.ensure_within_workspace(path)
        target.mkdir(parents=True, exist_ok=True)
        self.logger.info("Created folder", path=str(target))
        return {"success": True, "message": "Folder created.", "path": str(target)}

    def create_file(self, path: str, content: str = "") -> dict[str, Any]:
        target = self.resolver.ensure_within_workspace(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        self.logger.info("Created file", path=str(target))
        return {"success": True, "message": "File created.", "path": str(target)}

    def read_file(self, path: str) -> dict[str, Any]:
        target = self.resolver.ensure_within_workspace(path)
        if not target.exists():
            raise NotFoundError("File does not exist")
        return {"success": True, "path": str(target), "content": target.read_text(encoding="utf-8")}

    def write_file(self, path: str, content: str) -> dict[str, Any]:
        target = self.resolver.ensure_within_workspace(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        self.logger.info("Wrote file", path=str(target))
        return {"success": True, "message": "File written.", "path": str(target)}
