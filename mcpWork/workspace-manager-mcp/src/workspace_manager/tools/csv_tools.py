from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


class CsvTools:
    """Create and manipulate CSV files within the workspace."""

    def __init__(self, workspace_root: str | Path | None = None) -> None:
        self.workspace_root = Path(workspace_root or "workspace").resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, relative_path: str | Path) -> Path:
        candidate = (self.workspace_root / Path(relative_path)).resolve()
        candidate.relative_to(self.workspace_root)
        return candidate

    def create_csv(self, path: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
        resolved = self._resolve(path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        if rows:
            fieldnames = list(rows[0].keys())
            with resolved.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        else:
            resolved.write_text("", encoding="utf-8")
        return {"success": True, "path": str(resolved), "rows": rows}

    def append_csv(self, path: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
        resolved = self._resolve(path)
        if not resolved.exists():
            return self.create_csv(path, rows)
        with resolved.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writerows(rows)
        return {"success": True, "path": str(resolved), "rows": rows}

    def read_csv(self, path: str) -> dict[str, Any]:
        resolved = self._resolve(path)
        with resolved.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return {"success": True, "path": str(resolved), "rows": rows}

    def filter_csv(self, path: str, field: str, value: Any) -> dict[str, Any]:
        rows = self.read_csv(path)["rows"]
        filtered = [row for row in rows if row.get(field) == str(value)]
        return {"success": True, "path": path, "rows": filtered}

    def merge_csv(self, path: str, other_path: str) -> dict[str, Any]:
        rows = self.read_csv(path)["rows"] + self.read_csv(other_path)["rows"]
        return self.create_csv(path, rows)
