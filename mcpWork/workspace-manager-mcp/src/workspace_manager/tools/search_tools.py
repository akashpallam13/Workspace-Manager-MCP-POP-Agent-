from __future__ import annotations

from pathlib import Path
from typing import Any


class SearchTools:
    """Find files and content inside the workspace."""

    def __init__(self, workspace_root: str | Path | None = None) -> None:
        self.workspace_root = Path(workspace_root or "workspace").resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def find_files(self, pattern: str) -> dict[str, Any]:
        matches = [str(path.relative_to(self.workspace_root)) for path in self.workspace_root.rglob(pattern)]
        return {"success": True, "matches": matches}

    def search_content(self, term: str) -> dict[str, Any]:
        hits: list[dict[str, Any]] = []
        for path in self.workspace_root.rglob("*"):
            if path.is_file():
                try:
                    text = path.read_text(encoding="utf-8")
                except Exception:
                    continue
                if term in text:
                    hits.append({"path": str(path.relative_to(self.workspace_root)), "line": text.splitlines()[0]})
        return {"success": True, "hits": hits}
