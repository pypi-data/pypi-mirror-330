# Product Context: WCGW MCP Server

## Why This Project Exists

The WCGW (What Could Go Wrong) project is an MCP server that empowers AI assistants like Claude and ChatGPT to interact with and operate on a user's local machine. By providing a structured and secure interface, it enables these AI systems to perform real-world tasks such as:

- Executing shell commands
- Reading and writing files
- Editing code and documents
- Managing background processes
- Saving and restoring context between sessions

This bridges the gap between powerful language models and practical computing tasks, allowing AI assistants to help users with real-world development and automation tasks directly on their machines.

## Problems It Solves

1. **Limited AI Interaction**: Without WCGW, AI assistants cannot interact with the user's local environment, severely limiting their practical utility.

2. **Context Limitations**: AI assistants typically lose context between sessions; WCGW provides mechanisms for saving and restoring context.

3. **Platform Limitations**: Previously, the tool was limited to Unix-based systems (macOS and Linux); our recent work has added Windows compatibility.

4. **File Management Challenges**: Managing large files and complex edits is difficult in a chat interface; WCGW provides specialized tools for efficient file operations.

5. **Command Execution**: Running and monitoring commands, especially long-running or interactive ones, is challenging without proper tooling.

## How It Works

WCGW operates as a Model Context Protocol (MCP) server that:

1. **Registers Tools**: Exposes a set of standardized tools to the AI assistant:
   - BashCommand: Execute shell commands with timeout control
   - WriteIfEmpty: Create new files or write to empty files
   - FileEdit: Edit existing files using search/replace blocks
   - ReadFiles: Read content from one or more files
   - ReadImage: Read image files for display/processing
   - Initialize: Reset shell and set up workspace environment
   - ContextSave: Save project context for knowledge transfer

2. **Manages Resources**: Handles file system access, shell interactions, and background processes.

3. **Cross-Platform Operation**: Works across Windows, macOS, and Linux with consistent behavior.

4. **Security and Safety**: Implements protections like:
   - Requiring file reading before allowing edits to prevent accidental overwrites
   - Syntax checking on file edits
   - Restricting commands based on modes (architect, code-writer, wcgw)

5. **Real-time Feedback**: Provides real-time feedback to the AI assistant about command execution, file operations, and errors.

The system is designed to be robust, efficient, and maintainable while providing powerful capabilities to AI assistants in a secure manner.