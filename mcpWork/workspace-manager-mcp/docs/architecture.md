# Architecture Overview

The Workspace Manager MCP server is organized around a thin server entry point and a set of focused agents:

- WorkspaceAgent: project, folder, and file operations
- PlannerAgent: turns natural-language intent into structured actions
- TemplateAgent: generates starter template structures
- DatasetAgent: creates dataset folders for classification and detection tasks
- DocumentationAgent: scaffolds documentation files

Security and path handling are centralized in the security and path-resolution modules so every operation is validated before it reaches the filesystem.
