from __future__ import annotations

import shutil
import zipfile
from pathlib import Path
from typing import Any


class ZipTools:
    """Create and extract zip archives within the workspace."""

    def __init__(self, workspace_root: str | Path | None = None) -> None:
        self.workspace_root = Path(workspace_root or "workspace").resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, relative_path: str | Path) -> Path:
        candidate = (self.workspace_root / Path(relative_path)).resolve()
        candidate.relative_to(self.workspace_root)
        return candidate

    def compress_folder(self, folder: str) -> dict[str, Any]:
        source = self._resolve(folder)
        archive_path = source.with_suffix(".zip")
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in source.rglob("*"):
                if path.is_file():
                    archive.write(path, path.relative_to(source))
        return {"success": True, "path": str(archive_path), "message": "Folder archived."}

    def extract_zip(self, archive_path: str, destination: str | None = None) -> dict[str, Any]:
        source = self._resolve(archive_path)
        target = self._resolve(destination or source.stem)
        with zipfile.ZipFile(source, "r") as archive:
            archive.extractall(target)
        return {"success": True, "path": str(target), "message": "Archive extracted."}
