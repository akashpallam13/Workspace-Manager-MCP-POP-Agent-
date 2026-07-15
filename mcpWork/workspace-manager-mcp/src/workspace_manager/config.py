from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    import tomli as tomllib

from .models import WorkspaceConfig


class ConfigLoader:
    """Load workspace configuration from TOML."""

    def __init__(self, config_path: str | Path | None = None) -> None:
        self.config_path = Path(config_path or "config.toml")

    def load(self) -> WorkspaceConfig:
        if self.config_path.exists():
            with self.config_path.open("rb") as handle:
                raw = tomllib.load(handle)
            return WorkspaceConfig(**raw)
        return WorkspaceConfig()
