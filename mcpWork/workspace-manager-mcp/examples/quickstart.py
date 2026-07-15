from workspace_manager.server import create_server

if __name__ == "__main__":
    server = create_server()
    print("Workspace Manager MCP server initialized")
    server.run()
