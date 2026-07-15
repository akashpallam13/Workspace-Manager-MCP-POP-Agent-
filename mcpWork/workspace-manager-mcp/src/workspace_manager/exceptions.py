from __future__ import annotations


class WorkspaceError(Exception):
    """Base exception for workspace operations."""


class PathValidationError(WorkspaceError):
    """Raised when a path is invalid or escapes the workspace."""


class NotFoundError(WorkspaceError):
    """Raised when a requested resource does not exist."""


class AlreadyExistsError(WorkspaceError):
    """Raised when a resource already exists."""
