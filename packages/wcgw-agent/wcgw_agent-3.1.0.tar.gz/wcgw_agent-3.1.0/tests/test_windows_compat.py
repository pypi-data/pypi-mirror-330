import os
import tempfile
import sys
import time
import platform
from typing import Generator

import pytest

# Add the src directory to Python path if needed
if os.path.abspath('src') not in sys.path:
    sys.path.insert(0, os.path.abspath('src'))

from wcgw.client.bash_state.bash_state import BashState
from wcgw.client.platform_utils import (
    is_windows,
    is_mac,
    is_unix_like,
    get_default_shell,
    get_shell_launch_args,
    get_prompt_string
)
from wcgw.client.tools import (
    BashCommand,
    Context,
    ContextSave,
    Initialize,
    ReadFiles,
    ReadImage,
    WriteIfEmpty,
    default_enc,
    get_tool_output,
    which_tool_name,
)
from wcgw.types_ import (
    Command,
    Console,
    FileEdit,
    SendAscii,
    SendSpecials,
    SendText,
    StatusCheck,
)

# Skip all tests if not on Windows
pytestmark = pytest.mark.skipif(not is_windows(), reason="Windows-specific tests")


class TestConsole(Console):
    def __init__(self):
        self.logs = []
        self.prints = []

    def log(self, msg: str) -> None:
        self.logs.append(msg)
        print(f"[LOG] {msg}")

    def print(self, msg: str) -> None:
        self.prints.append(msg)
        print(f"[PRINT] {msg}")


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """Provides a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as td:
        yield td


@pytest.fixture
def context(temp_dir: str) -> Generator[Context, None, None]:
    """Provides a test context with temporary directory and handles cleanup."""
    console = TestConsole()
    bash_state = BashState(
        console=console,
        working_dir=temp_dir,
        bash_command_mode=None,
        file_edit_mode=None,
        write_if_empty_mode=None,
        mode=None,
        use_screen=True,  # This will use our Windows background process as we're on Windows
    )
    ctx = Context(
        bash_state=bash_state,
        console=console,
    )
    yield ctx
    # Cleanup after each test
    try:
        bash_state.sendintr()  # Send Ctrl-C to any running process
        bash_state.reset_shell()  # Reset shell state
        bash_state.cleanup()  # Cleanup final shell
    except Exception as e:
        print(f"Error during cleanup: {e}")


def test_platform_detection():
    """Verify Windows platform is detected correctly."""
    assert is_windows() is True
    assert is_mac() is False
    assert is_unix_like() is False
    
    # Test shell-related functions
    shell = get_default_shell()
    assert "powershell.exe" in shell.lower() or "cmd.exe" in shell.lower()
    
    prompt = get_prompt_string()
    assert prompt == ">"


def test_initialize(context: Context, temp_dir: str) -> None:
    """Test the Initialize tool with various configurations on Windows."""
    # Test default wcgw mode
    init_args = Initialize(
        type="first_call",
        any_workspace_path=temp_dir,
        initial_files_to_read=[],
        task_id_to_resume="",
        mode_name="wcgw",
        code_writer_config=None,
    )

    outputs, _ = get_tool_output(
        context, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )

    assert len(outputs) == 1
    assert isinstance(outputs[0], str)
    assert temp_dir in outputs[0]
    assert "System:" in outputs[0]
    assert "Windows" in outputs[0]  # Should mention Windows platform


def test_windows_path_handling(context: Context, temp_dir: str) -> None:
    """Test Windows-specific path handling."""
    # First initialize
    init_args = Initialize(
        type="first_call",
        any_workspace_path=temp_dir,
        initial_files_to_read=[],
        task_id_to_resume="",
        mode_name="wcgw",
        code_writer_config=None,
    )
    get_tool_output(context, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None)
    
    # Test path with backslashes
    test_file = os.path.join(temp_dir, "windows_path_test.txt")
    backslash_path = test_file.replace("/", "\\")
    
    # Write to file using Windows path
    write_args = WriteIfEmpty(file_path=backslash_path, file_content="Windows path test\r\n")
    outputs, _ = get_tool_output(
        context, write_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "Success" in outputs[0]
    
    # Read the file back
    read_args = ReadFiles(file_paths=[backslash_path])
    outputs, _ = get_tool_output(
        context, read_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "Windows path test" in outputs[0]
    
    # Test with spaces in path
    space_dir = os.path.join(temp_dir, "Path With Spaces")
    os.makedirs(space_dir, exist_ok=True)
    space_file = os.path.join(space_dir, "space test.txt")
    
    # Write to file with spaces in path
    write_args = WriteIfEmpty(file_path=space_file, file_content="Path with spaces test\r\n")
    outputs, _ = get_tool_output(
        context, write_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "Success" in outputs[0]
    
    # Read the file back
    read_args = ReadFiles(file_paths=[space_file])
    outputs, _ = get_tool_output(
        context, read_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "Path with spaces test" in outputs[0]


def test_windows_commands(context: Context, temp_dir: str) -> None:
    """Test Windows-specific commands."""
    # First initialize
    init_args = Initialize(
        type="first_call",
        any_workspace_path=temp_dir,
        initial_files_to_read=[],
        task_id_to_resume="",
        mode_name="wcgw",
        code_writer_config=None,
    )
    get_tool_output(context, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None)
    
    # Test dir command
    cmd = BashCommand(action_json=Command(command="dir"))
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert isinstance(outputs[0], str)
    assert "Directory of" in outputs[0] or "Volume in drive" in outputs[0]
    
    # Test echo with Windows-style quotes
    cmd = BashCommand(action_json=Command(command='echo "Windows test"'))
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "Windows test" in outputs[0]
    
    # Test Windows timeout command
    cmd = BashCommand(action_json=Command(command="timeout /t 1"), wait_for_seconds=0.5)
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert "status = still running" in outputs[0]
    
    # Wait for command to complete
    time.sleep(2)
    
    # Check status
    status_check = BashCommand(action_json=StatusCheck(status_check=True))
    outputs, _ = get_tool_output(
        context, status_check, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "status = process exited" in outputs[0]


def test_windows_file_operations(context: Context, temp_dir: str) -> None:
    """Test file operations on Windows."""
    # First initialize
    init_args = Initialize(
        type="first_call",
        any_workspace_path=temp_dir,
        initial_files_to_read=[],
        task_id_to_resume="",
        mode_name="wcgw",
        code_writer_config=None,
    )
    get_tool_output(context, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None)
    
    # Test writing a file with Windows line endings
    test_file = os.path.join(temp_dir, "windows_test.txt")
    write_args = WriteIfEmpty(file_path=test_file, file_content="Line 1\r\nLine 2\r\nLine 3\r\n")
    outputs, _ = get_tool_output(
        context, write_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "Success" in outputs[0]
    
    # Test reading the file back
    read_args = ReadFiles(file_paths=[test_file])
    outputs, _ = get_tool_output(
        context, read_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "Line 1" in outputs[0]
    assert "Line 2" in outputs[0]
    assert "Line 3" in outputs[0]
    
    # Use Windows type command to read file
    cmd = BashCommand(action_json=Command(command=f'type "{test_file}"'))
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "Line 1" in outputs[0]
    assert "Line 2" in outputs[0]
    assert "Line 3" in outputs[0]


def test_interaction_commands(context: Context, temp_dir: str) -> None:
    """Test the various interaction command types on Windows."""
    # First initialize
    init_args = Initialize(
        type="first_call",
        any_workspace_path=temp_dir,
        initial_files_to_read=[],
        task_id_to_resume="",
        mode_name="wcgw",
        code_writer_config=None,
    )
    get_tool_output(context, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None)

    # Test text interaction
    cmd = BashCommand(action_json=SendText(send_text="echo hello"))
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    assert len(outputs) == 1
    assert isinstance(outputs[0], str)

    # Test special keys (Enter)
    cmd = BashCommand(action_json=SendSpecials(send_specials=["Enter"]))
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    assert len(outputs) == 1
    assert isinstance(outputs[0], str)
    assert "hello" in outputs[0].lower()

    # Test long-running command interruption
    cmd = BashCommand(action_json=Command(command="timeout /t 5"), wait_for_seconds=0.1)
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    assert "status = still running" in outputs[0]

    # Send Ctrl-C
    cmd = BashCommand(action_json=SendSpecials(send_specials=["Ctrl-c"]))
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    assert len(outputs) == 1
    assert "status = process exited" in outputs[0]


def test_windows_background_process(context: Context, temp_dir: str) -> None:
    """Test Windows background process management."""
    # First initialize
    init_args = Initialize(
        type="first_call",
        any_workspace_path=temp_dir,
        initial_files_to_read=[],
        task_id_to_resume="",
        mode_name="wcgw",
        code_writer_config=None,
    )
    get_tool_output(context, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None)
    
    # Create a file for testing
    test_file = os.path.join(temp_dir, "bg_test.txt")
    
    # Start a background process
    cmd = BashCommand(
        action_json=Command(
            command=f'echo "Background process running" > "{test_file}" & timeout /t 5'
        ), 
        wait_for_seconds=0.1
    )
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert "status = still running" in outputs[0]
    
    # Wait a bit for the command to execute
    time.sleep(2)
    
    # Verify file was created
    assert os.path.exists(test_file)
    with open(test_file, "r") as f:
        content = f.read()
    assert "Background process running" in content
    
    # Test process termination
    cmd = BashCommand(action_json=SendSpecials(send_specials=["Ctrl-c"]))
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert "status = process exited" in outputs[0]


def test_error_cases(context: Context, temp_dir: str) -> None:
    """Test various error cases on Windows."""
    # First initialize
    init_args = Initialize(
        type="first_call",
        any_workspace_path=temp_dir,
        initial_files_to_read=[],
        task_id_to_resume="",
        mode_name="wcgw",
        code_writer_config=None,
    )
    get_tool_output(context, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None)

    # Test reading non-existent file
    read_args = ReadFiles(file_paths=[os.path.join(temp_dir, "nonexistent.txt")])
    outputs, _ = get_tool_output(
        context, read_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    assert len(outputs) == 1
    assert "Error" in outputs[0]

    # Test writing to non-existent directory
    write_args = WriteIfEmpty(
        file_path=os.path.join(temp_dir, "nonexistent", "test.txt"), file_content="test"
    )
    outputs, _ = get_tool_output(
        context, write_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    assert len(outputs) == 1
    assert "Success" in outputs[0]  # Should succeed as it creates directories

    # Test invalid Windows command
    cmd = BashCommand(action_json=Command(command="nonexistentcommand"))
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    assert len(outputs) == 1
    assert "not recognized" in str(outputs[0]).lower() or "not found" in str(outputs[0]).lower()
    
    # Test command with illegal characters for Windows
    cmd = BashCommand(action_json=Command(command="echo test > file<>:.txt"))
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    assert len(outputs) == 1
    assert "error" in str(outputs[0]).lower() or "invalid" in str(outputs[0]).lower()


def test_windows_special_features(context: Context, temp_dir: str) -> None:
    """Test Windows-specific features like long paths and network paths."""
    # First initialize
    init_args = Initialize(
        type="first_call",
        any_workspace_path=temp_dir,
        initial_files_to_read=[],
        task_id_to_resume="",
        mode_name="wcgw",
        code_writer_config=None,
    )
    get_tool_output(context, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None)
    
    # Test a very deep path structure (long path support)
    deep_path = os.path.join(temp_dir, "depth1", "depth2", "depth3", "depth4", "depth5", 
                           "depth6", "depth7", "depth8", "depth9", "depth10")
    os.makedirs(deep_path, exist_ok=True)
    
    deep_file = os.path.join(deep_path, "deep_file.txt")
    write_args = WriteIfEmpty(file_path=deep_file, file_content="Deep path test\r\n")
    outputs, _ = get_tool_output(
        context, write_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "Success" in outputs[0]
    
    # Read the file back
    read_args = ReadFiles(file_paths=[deep_file])
    outputs, _ = get_tool_output(
        context, read_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "Deep path test" in outputs[0]
    
    # Test using the Windows dir command on the deep path
    cmd = BashCommand(action_json=Command(command=f'dir "{deep_path}"'))
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "deep_file.txt" in outputs[0]

    
# Run the tests if script is executed directly
if __name__ == "__main__":
    pytest.main(["-xvs", __file__])