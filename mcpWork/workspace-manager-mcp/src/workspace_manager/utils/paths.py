from __future__ import annotations

from pathlib import Path

from ..exceptions import PathValidationError


class WorkspacePathResolver:
    """Resolve and validate workspace-relative paths."""

    def __init__(self, workspace_root: str | Path) -> None:
        self.workspace_root = Path(workspace_root).resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def resolve(self, path: str | Path) -> Path:
        candidate = Path(path).expanduser()
        if candidate.is_absolute():
            resolved = candidate.resolve(strict=False)
        else:
            resolved = (self.workspace_root / candidate).resolve(strict=False)

        try:
            resolved.relative_to(self.workspace_root)
        except ValueError as exc:
            raise PathValidationError("Path escapes the workspace root") from exc

        return resolved

    def ensure_within_workspace(self, path: str | Path) -> Path:
        return self.resolve(path)
