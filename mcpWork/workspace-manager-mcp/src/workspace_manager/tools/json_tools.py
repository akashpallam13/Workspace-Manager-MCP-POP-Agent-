from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonTools:
    """Handle JSON file operations safely inside the workspace."""

    def __init__(self, workspace_root: str | Path | None = None) -> None:
        self.workspace_root = Path(workspace_root or "workspace").resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, relative_path: str | Path) -> Path:
        candidate = (self.workspace_root / Path(relative_path)).resolve()
        candidate.relative_to(self.workspace_root)
        return candidate

    def read_json(self, path: str) -> dict[str, Any]:
        resolved = self._resolve(path)
        with resolved.open("r", encoding="utf-8") as handle:
            return {"success": True, "path": str(resolved), "data": json.load(handle)}

    def write_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        resolved = self._resolve(path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        with resolved.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        return {"success": True, "path": str(resolved), "message": "JSON written."}

    def update_json(self, path: str, updates: dict[str, Any]) -> dict[str, Any]:
        existing = self.read_json(path)["data"]
        existing.update(updates)
        return self.write_json(path, existing)

    def merge_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        existing = self.read_json(path)["data"]
        if not isinstance(existing, dict) or not isinstance(payload, dict):
            return {"success": False, "message": "Both sources must be objects."}
        existing.update(payload)
        return self.write_json(path, existing)

    def pretty_print_json(self, path: str) -> dict[str, Any]:
        data = self.read_json(path)["data"]
        return {"success": True, "path": path, "pretty": json.dumps(data, indent=2)}
