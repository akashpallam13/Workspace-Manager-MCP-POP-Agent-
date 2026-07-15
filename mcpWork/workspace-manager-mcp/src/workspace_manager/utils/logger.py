from __future__ import annotations

import logging
from typing import Any


class WorkspaceLogger:
    """Simple structured logger wrapper."""

    def __init__(self, name: str = "workspace_manager", level: str = "INFO") -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
            self.logger.addHandler(handler)

    def info(self, message: str, **context: Any) -> None:
        self.logger.info("%s %s", message, context)

    def warning(self, message: str, **context: Any) -> None:
        self.logger.warning("%s %s", message, context)

    def error(self, message: str, **context: Any) -> None:
        self.logger.error("%s %s", message, context)
