from __future__ import annotations

from pathlib import Path
from typing import Any


class FolderTools:
    """Basic folder management helpers."""

    def __init__(self, workspace_root: str | Path | None = None) -> None:
        self.workspace_root = Path(workspace_root or "workspace").resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def create_folder(self, relative_path: str) -> dict[str, Any]:
        target = (self.workspace_root / relative_path).resolve()
        target.mkdir(parents=True, exist_ok=True)
        return {"success": True, "path": str(target)}

    def list_folder(self, relative_path: str = ".") -> dict[str, Any]:
        target = (self.workspace_root / relative_path).resolve()
        entries = [entry.name for entry in target.iterdir()]
        return {"success": True, "path": str(target), "entries": entries}
