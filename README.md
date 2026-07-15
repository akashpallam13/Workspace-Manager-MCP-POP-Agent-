# Workspace Manager MCP

Workspace Manager MCP is a secure, modular Python MCP server for creating, organizing, editing, and managing AI projects inside a dedicated workspace directory. It is designed as a safe, policy-driven workspace assistant rather than a general-purpose file browser.

All operations stay inside a protected workspace root and reject paths that try to escape it. The project is intentionally layered so agents, tools, security rules, and configuration can evolve independently.

## What the project includes

### Project and workspace management
- Create, list, and remove projects
- Create and manage folders and files inside each project
- Read, write, append, copy, and delete files safely within the workspace

### Structured data tools
- Read and write JSON files
- Create, append, read, and inspect CSV files
- Search for files or content across the workspace
- Create and extract ZIP archives for simple backup and packaging workflows

### Planning and automation support
- Interpret natural-language prompts such as “create a React app” or “create a YOLO project”
- Return a structured plan for the requested workflow
- Support expansion for more complex planning and agent-driven actions

### Dataset and template support
- Generate dataset folder structures for common ML tasks
- Provide starter template ideas for Python, React, FastAPI, AI, YOLO, research, and documentation projects

### Security model
- Restricts all file system access to a dedicated workspace directory
- Blocks path traversal and directory escape attempts
- Rejects unsafe names and disallowed system locations
- Uses centralized validation before any write or read operation

## Local installation

### 1. Prerequisites
Make sure you have Python 3.10+ available. The project is written to be compatible with the current environment and tested with pytest.

### 2. Clone or open the project
```bash
cd /path/to/your/workspace
git clone <your-repo-url>
cd workspace-manager-mcp
```

### 3. Create a virtual environment
On Windows:
```powershell
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -e .[dev]
```

### 5. Run the server
```bash
python -m workspace_manager.server
```

## Example usage

### Create a project and a file
```python
from workspace_manager.server import create_server

server = create_server()
print(server)
```

### Use the workspace agent directly
```python
from workspace_manager.agents.workspace_agent import WorkspaceAgent
from workspace_manager.models import WorkspaceConfig
from workspace_manager.security import SecurityGuard
from workspace_manager.utils.logger import WorkspaceLogger

config = WorkspaceConfig(workspace_root="workspace")
agent = WorkspaceAgent(config, SecurityGuard(config.resolve_workspace_root()), WorkspaceLogger())
agent.create_project("demo")
agent.create_file("demo/README.md", "Hello from Workspace Manager MCP")
```

### Use the file and archive helpers
```python
from workspace_manager.tools.file_tools import FileTools
from workspace_manager.tools.zip_tools import ZipTools

workspace = "."
file_tools = FileTools(workspace_root=workspace)
zip_tools = ZipTools(workspace_root=workspace)

file_tools.create_file("notes.txt", "hello")
file_tools.append_file("notes.txt", " world")
zip_tools.compress_folder(".")
```

## Configuration
The project uses a TOML configuration file named config.toml. You can change the workspace root, logging level, allowed extensions, and template directory there.

## Testing
Run the tests locally with:
```bash
python -m pytest -q
```

## Project structure
- src/workspace_manager: main package
- src/workspace_manager/agents: planner, workspace, template, dataset, and documentation agents
- src/workspace_manager/tools: JSON, CSV, search, file, and ZIP helpers
- tests: pytest coverage for safe workspace behavior and core tool operations
- docs: architecture notes and usage guidance

## Architecture notes
The server is organized around a small set of cooperating modules:
- SecurityGuard validates all requested paths before access
- WorkspaceAgent and the planner agents provide high-level operations
- Tool modules implement focused file, JSON, CSV, search, and archive workflows
- DatasetAgent scaffolds machine-learning-ready folder layouts and a starter README

## Next steps
This project is now a solid foundation for a secure AI workspace manager. It is ready for further extension with richer templates, semantic search, metadata inspection, and more automation-oriented agents.
