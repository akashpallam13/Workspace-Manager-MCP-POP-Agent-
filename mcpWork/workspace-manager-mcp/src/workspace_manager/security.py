from __future__ import annotations

from pathlib import Path

from .exceptions import PathValidationError


class SecurityGuard:
    """Validate file paths and names before mutating the workspace."""

    def __init__(self, workspace_root: str | Path) -> None:
        self.workspace_root = Path(workspace_root).resolve()

    def validate_path(self, path: str | Path) -> Path:
        candidate = Path(path).expanduser()
        if candidate.is_absolute():
            resolved = candidate.resolve(strict=False)
        else:
            resolved = (self.workspace_root / candidate).resolve(strict=False)

        if not self._is_safe(resolved):
            raise PathValidationError("Path is unsafe or escapes the workspace")
        return resolved

    def validate_name(self, name: str) -> str:
        forbidden = {".", "..", "", "/", "\\"}
        if name in forbidden or any(part in {"Desktop", "Documents", "Downloads", "Pictures", "Videos", "Windows", "Program Files", "AppData"} for part in name.split("/")):
            raise PathValidationError("Unsafe filename")
        return name

    def _is_safe(self, path: Path) -> bool:
        try:
            path.relative_to(self.workspace_root)
        except ValueError:
            return False
        if any(part in {"Desktop", "Documents", "Downloads", "Pictures", "Videos", "Windows", "Program Files", "AppData"} for part in path.parts):
            return False
        if any(part.startswith(".") for part in path.parts):
            return False
        return True
