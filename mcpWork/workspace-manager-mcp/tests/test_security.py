from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from workspace_manager.exceptions import PathValidationError
from workspace_manager.security import SecurityGuard


def test_path_escape_is_rejected() -> None:
    with TemporaryDirectory() as tmp_dir:
        guard = SecurityGuard(tmp_dir)
        with pytest.raises(PathValidationError):
            guard.validate_path(str(Path(tmp_dir).parent / "outside.txt"))
