from pathlib import Path
from tempfile import TemporaryDirectory

from workspace_manager.tools.json_tools import JsonTools
from workspace_manager.tools.csv_tools import CsvTools


def test_json_tools_round_trip() -> None:
    with TemporaryDirectory() as tmp_dir:
        tools = JsonTools(workspace_root=tmp_dir)
        result = tools.write_json("config.json", {"name": "demo", "enabled": True})
        assert result["success"] is True
        read_result = tools.read_json("config.json")
        assert read_result["data"]["name"] == "demo"
        update_result = tools.update_json("config.json", {"version": 1})
        assert update_result["success"] is True


def test_csv_tools_round_trip() -> None:
    with TemporaryDirectory() as tmp_dir:
        tools = CsvTools(workspace_root=tmp_dir)
        create_result = tools.create_csv("data.csv", [{"name": "Alice", "age": 30}])
        assert create_result["success"] is True
        append_result = tools.append_csv("data.csv", [{"name": "Bob", "age": 40}])
        assert append_result["success"] is True
        read_result = tools.read_csv("data.csv")
        assert len(read_result["rows"]) == 2
