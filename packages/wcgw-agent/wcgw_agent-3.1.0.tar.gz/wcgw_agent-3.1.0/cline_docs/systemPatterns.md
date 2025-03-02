# System Patterns: WCGW Architecture

## Core Architectural Patterns

### MCP Server Architecture
- Implements the Model Context Protocol specification
- Exposes standardized tools and resources to AI assistants
- Uses stdio-based communication with the Claude desktop app
- Structured as a request-response server with defined schemas

### Platform Abstraction Layer
- Isolates platform-specific functionality behind common interfaces
- Uses detection utilities in `platform_utils.py` for runtime platform determination
- Implements platform-specific functionality while maintaining consistent interfaces
- Primary example: `ShellHandler` class with platform-specific implementations

### Command Pattern
- Encapsulates shell commands as objects
- Handles command execution, monitoring, and result processing
- Provides timeout and cancellation mechanisms
- Manages interactive command input and output

## Key Implementation Patterns

### Factory Method Pattern
- Used to create appropriate handlers based on platform
- Example: `ShellHandler.create_handler()` returns the correct implementation for the detected platform
- Allows client code to work with abstractions without knowing concrete implementations

### Strategy Pattern
- Different strategies for handling shells on different platforms
- Variation in how commands are executed, monitored, and terminated
- Common interface allows interchangeable use

### Adapter Pattern
- Windows implementation adapts subprocess-based shell interaction to match the Pexpect interface
- Provides consistent expect/send interface despite platform differences
- Translates between different platform-specific APIs

### Facade Pattern
- High-level tools provide simplified interfaces to complex subsystems
- Example: `BashCommand` tool provides a simple interface to the complex shell interaction system
- Hides implementation complexity from the AI assistant

## File Operation Patterns

### Template Method Pattern
- Common file operation workflows with platform-specific steps
- Defined sequence of operations with hooks for platform-specific behavior
- Examples in file path handling and editing operations

### Decorator Pattern
- Adds additional functionality to basic file operations
- Examples include syntax checking, chunking for large files, and preview generation

## Error Handling and Safety

### Circuit Breaker Pattern
- Prevents cascading failures
- Imposes timeouts and automatic cancellation
- Protects system resources during problematic operations

### Sandbox Pattern
- Restricts operations based on operation mode (architect, code-writer, wcgw)
- Implements permission checking for file operations
- Prevents accidental file overwrites through read-before-write enforcement

## Cross-Platform Implementation

### Background Process Management
- Unix: Uses 'screen' for terminal multiplexing
- Windows: Custom implementation using subprocess and Windows process management

### Interactive Shell Handling
- Unix: Leverages Pexpect for terminal interaction
- Windows: Custom expect-like implementation using subprocess and pipes

### File Path Operations
- Abstracts operating system path differences
- Handles different path separators and conventions
- Normalizes paths for consistent handling