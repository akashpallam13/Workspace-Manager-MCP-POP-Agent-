from __future__ import annotations

from pathlib import Path
from typing import Any


class ProjectTools:
    """High-level project lifecycle helpers."""

    def __init__(self, workspace_root: str | Path | None = None) -> None:
        self.workspace_root = Path(workspace_root or "workspace").resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def create_project(self, name: str) -> dict[str, Any]:
        target = self.workspace_root / name
        target.mkdir(parents=True, exist_ok=False)
        return {"success": True, "project": name, "path": str(target)}

    def list_projects(self) -> dict[str, Any]:
        projects = [p.name for p in self.workspace_root.iterdir() if p.is_dir()]
        return {"success": True, "projects": projects}

    def delete_project(self, name: str) -> dict[str, Any]:
        target = self.workspace_root / name
        if target.exists():
            for child in sorted(target.rglob("*"), reverse=True):
                if child.is_file() or child.is_symlink():
                    child.unlink()
                elif child.is_dir():
                    child.rmdir()
            target.rmdir()
        return {"success": True, "project": name, "message": "Project removed."}
