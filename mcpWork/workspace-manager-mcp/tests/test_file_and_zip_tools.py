from pathlib import Path
from tempfile import TemporaryDirectory

from workspace_manager.tools.file_tools import FileTools
from workspace_manager.tools.zip_tools import ZipTools


def test_file_and_zip_round_trip() -> None:
    with TemporaryDirectory() as tmp_dir:
        file_tools = FileTools(workspace_root=tmp_dir)
        zip_tools = ZipTools(workspace_root=tmp_dir)

        file_tools.create_file("demo.txt", "hello")
        result = file_tools.read_file("demo.txt")
        assert result["content"] == "hello"

        file_tools.create_file("nested/notes.txt", "world")
        file_tools.copy_file("nested/notes.txt", "copied.txt")
        assert Path(tmp_dir, "copied.txt").exists()

        archive_result = zip_tools.compress_folder(".")
        assert archive_result["success"] is True
