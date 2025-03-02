# Technical Context: WCGW

## Technologies Used

### Core Technologies
- **Python 3.11+**: Primary development language
- **Model Context Protocol (MCP)**: Communication protocol for AI assistants
- **Shell Interaction**:
  - Unix: Pexpect for terminal interaction
  - Windows: Subprocess and custom expect-like implementation
- **File System Operations**: Python's os and pathlib modules

### Dependencies
From pyproject.toml:
- **openai>=1.46.0**: OpenAI API client
- **typer>=0.12.5**: CLI application building
- **rich>=13.8.1**: Terminal formatting and display
- **python-dotenv>=1.0.1**: Environment variable management
- **shell>=1.0.1**: Shell utilities
- **toml>=0.10.2**: TOML file parsing
- **petname>=2.6**: Name generation
- **pyte>=0.8.2**: Terminal emulation
- **fastapi>=0.115.0**: API framework
- **uvicorn>=0.31.0**: ASGI server
- **websockets>=13.1**: WebSocket support
- **pydantic>=2.9.2**: Data validation
- **semantic-version>=2.10.0**: Version parsing
- **anthropic>=0.39.0**: Anthropic API client
- **tokenizers>=0.21.0**: Token counting
- **pygit2>=1.16.0**: Git operations
- **syntax-checker>=0.3.0**: Code syntax validation

**Platform-specific**:
- **pexpect>=4.9.0**: Terminal interaction (Unix-only)

## Development Setup

### Environment Setup
1. **Python Environment**:
   - Python 3.11 or higher required
   - Virtual environment recommended (venv, conda, or uv)

2. **Installation Methods**:
   - Development: Clone repository and install with `pip install -e .`
   - User: Install via pip or uv from PyPI

3. **Platform-specific Setup**:
   - **Unix (macOS/Linux)**:
     - Screen command required for terminal multiplexing
     - Bash or compatible shell
   - **Windows**:
     - PowerShell or Command Prompt
     - No external dependencies required

### Testing
- **pytest**: Test framework
- **pytest-cov**: Coverage reporting
- **pytest-asyncio**: Async test support

### Building
- **hatchling**: Build system for Python packages
- **Build process**: `python -m build`

## Technical Constraints

### Platform Compatibility
- **Unix Compatibility**: macOS and Linux fully supported
- **Windows Compatibility**: Full feature parity with Windows-specific implementations
- **Path Handling**: Platform-specific path differences must be handled carefully

### Security Constraints
- **File Protection**: Read-before-write protection for file safety
- **Mode Restrictions**: Different operational modes enforce different levels of restrictions

### Performance Considerations
- **Large File Handling**: Chunking for large files to avoid token limit issues
- **Long-running Commands**: Timeout mechanisms to prevent hanging

### Dependencies
- **Pexpect Dependency**: Unix-only, requires platform-specific handling
- **Screen Command**: Unix-only, requires Windows alternative implementation

## Development Workflow

### Version Control
- **Git**: Source control management
- **GitHub**: Hosting, CI/CD, issue tracking

### CI/CD Pipeline
- **GitHub Actions**:
  - Unit tests
  - Type checking (mypy)
  - Coverage reporting
  - Build verification

### Release Process
1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Build distribution files
4. Test on TestPyPI
5. Publish to PyPI
6. Create GitHub release

### Documentation
- **README.md**: Main documentation
- **CHANGELOG.md**: Version history
- **PUBLISHING.md**: Release instructions
- **Feature documentation**: In src/wcgw/client/docs/