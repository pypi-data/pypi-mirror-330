"""
Terminal Controller UVx Package - MCP server for terminal command execution
"""

from .core import (
    execute_command,
    get_command_history,
    get_current_directory,
    change_directory,
    list_directory,
    run_server
)

__version__ = "0.1.2"

def main():
    """Entry point for the Terminal Controller UVx package when installed via UVx"""
    # This function will be called when the package is run via the UVx system
    # or when the user runs the console script terminal-controller
    run_server()