from __future__ import annotations

from pathlib import Path
from typing import Any


class FileTools:
    """File operations within the workspace."""

    def __init__(self, workspace_root: str | Path | None = None) -> None:
        self.workspace_root = Path(workspace_root or "workspace").resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, relative_path: str | Path) -> Path:
        candidate = (self.workspace_root / Path(relative_path)).resolve()
        candidate.relative_to(self.workspace_root)
        return candidate

    def create_file(self, path: str, content: str = "") -> dict[str, Any]:
        resolved = self._resolve(path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(content, encoding="utf-8")
        return {"success": True, "path": str(resolved), "message": "File created."}

    def read_file(self, path: str) -> dict[str, Any]:
        resolved = self._resolve(path)
        return {"success": True, "path": str(resolved), "content": resolved.read_text(encoding="utf-8")}

    def write_file(self, path: str, content: str) -> dict[str, Any]:
        return self.create_file(path, content)

    def append_file(self, path: str, content: str) -> dict[str, Any]:
        resolved = self._resolve(path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        with resolved.open("a", encoding="utf-8") as handle:
            handle.write(content)
        return {"success": True, "path": str(resolved), "message": "Content appended."}

    def delete_file(self, path: str) -> dict[str, Any]:
        resolved = self._resolve(path)
        resolved.unlink(missing_ok=True)
        return {"success": True, "path": str(resolved), "message": "File deleted."}

    def copy_file(self, source: str, destination: str) -> dict[str, Any]:
        source_path = self._resolve(source)
        dest_path = self._resolve(destination)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_bytes(source_path.read_bytes())
        return {"success": True, "path": str(dest_path), "message": "File copied."}
