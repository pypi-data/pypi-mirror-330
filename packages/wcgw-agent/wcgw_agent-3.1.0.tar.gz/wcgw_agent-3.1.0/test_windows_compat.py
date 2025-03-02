import os
import platform
import pytest
import tempfile
import time
import sys
from typing import Generator

# Add the src directory to Python path
sys.path.insert(0, os.path.abspath('src'))

from wcgw.client.platform_utils import (
    is_windows,
    is_mac,
    is_unix_like,
    get_default_shell,
    get_shell_launch_args,
    get_prompt_string
)
from wcgw.client.bash_state.shell_handler import (
    ShellHandler,
    start_shell,
    cleanup_all_screens_with_name
)
from wcgw.client.bash_state.bash_state import BashState
from wcgw.client.tools import (
    Context,
    Initialize,
    BashCommand,
    ReadFiles,
    WriteIfEmpty,
    FileEdit,
    default_enc,
    get_tool_output
)
from wcgw.types_ import Command, Console, SendText, SendSpecials, StatusCheck

# Import Windows-specific modules if on Windows
if is_windows():
    from wcgw.client.bash_state.windows_bg_process import (
        create_background_process,
        list_background_processes,
        terminate_background_process
    )


class TestConsole(Console):
    """Test console implementation for logging test output."""
    
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
        use_screen=True,  # This will use screen on Unix and our Windows background process on Windows
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
    """Test that platform detection works correctly."""
    if platform.system() == "Windows":
        assert is_windows() is True
        assert is_mac() is False
        assert is_unix_like() is False
    elif platform.system() == "Darwin":
        assert is_windows() is False
        assert is_mac() is True
        assert is_unix_like() is True
    else:  # Linux or other Unix-like
        assert is_windows() is False
        assert is_mac() is False
        assert is_unix_like() is True


def test_shell_handler_creation():
    """Test creating a shell handler for the current platform."""
    shell_cmd = get_default_shell()
    shell_args = get_shell_launch_args(False)
    
    # Test that we get the correct shell for the platform
    if is_windows():
        assert "powershell.exe" in shell_cmd.lower() or "cmd.exe" in shell_cmd.lower()
    else:
        assert "bash" in shell_cmd or "sh" in shell_cmd or "zsh" in shell_cmd
    
    # Create shell handler
    shell = ShellHandler.create_handler(
        shell_cmd,
        env=os.environ.copy(),
        echo=True,
        encoding="utf-8",
        timeout=5.0,
        cwd=os.getcwd(),
    )
    
    # Test platform-specific handler type
    if is_windows():
        from wcgw.client.bash_state.shell_handler import WindowsShellHandler
        assert isinstance(shell, WindowsShellHandler)
    else:
        from wcgw.client.bash_state.shell_handler import PexpectShellHandler
        assert isinstance(shell, PexpectShellHandler)
    
    # Clean up
    shell.close(force=True)


@pytest.mark.skipif(not is_windows(), reason="Windows-specific test")
def test_windows_background_process():
    """Test Windows-specific background process management."""
    console = TestConsole()
    
    # Create a temporary directory for test files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test file
        test_file = os.path.join(temp_dir, "bg_test.txt")
        
        # Create a background process
        cmd = f'echo "Background process test" > "{test_file}" & timeout /t 2'
        proc_id = create_background_process(cmd, "test_process", console)
        
        assert proc_id is not None
        
        # Wait for the process to complete
        time.sleep(3)
        
        # Verify file was created
        assert os.path.exists(test_file)
        with open(test_file, "r") as f:
            content = f.read()
        assert "Background process test" in content
        
        # List processes
        processes = list_background_processes(console)
        
        # Test termination
        cmd = f'timeout /t 10'
        proc_id2 = create_background_process(cmd, "long_process", console)
        
        assert proc_id2 is not None
        
        # Verify process is in list
        processes = list_background_processes(console)
        assert any(p["id"] == proc_id2 for p in processes)
        
        # Terminate process
        result = terminate_background_process(proc_id2, console)
        assert result is True
        
        # Verify process is removed
        processes = list_background_processes(console)
        assert not any(p["id"] == proc_id2 for p in processes)


def test_initialize_tool(context, temp_dir):
    """Test the Initialize tool works across platforms."""
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
    
    # Platform-specific checks
    if is_windows():
        assert "Windows" in outputs[0]
    elif is_mac():
        assert "Darwin" in outputs[0]
    else:
        assert "Linux" in outputs[0] or "Unix" in outputs[0]


def test_bash_command(context, temp_dir):
    """Test the BashCommand tool works across platforms."""
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
    
    # Platform-specific echo command
    if is_windows():
        echo_cmd = 'echo "hello world"'
    else:
        echo_cmd = "echo 'hello world'"
    
    # Test simple command
    cmd = BashCommand(action_json=Command(command=echo_cmd))
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert isinstance(outputs[0], str)
    assert "hello world" in outputs[0]
    
    # Test long-running command with status check
    if is_windows():
        sleep_cmd = "timeout /t 2"
    else:
        sleep_cmd = "sleep 2"
    
    cmd = BashCommand(action_json=Command(command=sleep_cmd), wait_for_seconds=0.5)
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


def test_file_operations(context, temp_dir):
    """Test file operations work across platforms."""
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
    
    # Test writing a file
    test_file = os.path.join(temp_dir, "test.txt")
    write_args = WriteIfEmpty(file_path=test_file, file_content="test content\n")
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
    assert "test content" in outputs[0]
    
    # Test editing the file
    edit_args = FileEdit(
        file_path=test_file,
        file_edit_using_search_replace_blocks="""<<<<<<< SEARCH
test content
=======
edited content
>>>>>>> REPLACE""",
    )
    
    outputs, _ = get_tool_output(
        context, edit_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    
    # Verify the change
    with open(test_file) as f:
        content = f.read()
    assert "edited content" in content


def test_nested_paths(context, temp_dir):
    """Test that nested paths work correctly on the platform."""
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
    
    # Create nested directory structure
    nested_dir = os.path.join(temp_dir, "level1", "level2", "level3")
    os.makedirs(nested_dir, exist_ok=True)
    
    # Test writing to nested path
    test_file = os.path.join(nested_dir, "nested_test.txt")
    write_args = WriteIfEmpty(file_path=test_file, file_content="nested content\n")
    outputs, _ = get_tool_output(
        context, write_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "Success" in outputs[0]
    
    # Verify file was created
    assert os.path.exists(test_file)
    with open(test_file) as f:
        content = f.read()
    assert "nested content" in content
    
    # Test listing the directory tree
    if is_windows():
        list_cmd = "dir /s /b"
    else:
        list_cmd = "find . -type f | sort"
        
    cmd = BashCommand(action_json=Command(command=list_cmd))
    outputs, _ = get_tool_output(
        context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
    )
    
    assert len(outputs) == 1
    assert "nested_test.txt" in outputs[0]


if __name__ == "__main__":
    """Run the tests with pytest or as a standalone script."""
    if "pytest" in sys.modules:
        print("Running tests with pytest")
    else:
        # Run tests manually
        print("Running tests manually")
        
        # Create temporary test context
        with tempfile.TemporaryDirectory() as td:
            console = TestConsole()
            bash_state = BashState(
                console=console,
                working_dir=td,
                bash_command_mode=None,
                file_edit_mode=None,
                write_if_empty_mode=None,
                mode=None,
                use_screen=True,
            )
            context = Context(
                bash_state=bash_state,
                console=console,
            )
            
            try:
                print("\n=== Platform Detection Tests ===")
                test_platform_detection()
                print("✅ Platform detection tests passed")
                
                print("\n=== Shell Handler Tests ===")
                test_shell_handler_creation()
                print("✅ Shell handler tests passed")
                
                if is_windows():
                    print("\n=== Windows Background Process Tests ===")
                    test_windows_background_process()
                    print("✅ Windows background process tests passed")
                
                print("\n=== Initialize Tool Tests ===")
                test_initialize_tool(context, td)
                print("✅ Initialize tool tests passed")
                
                print("\n=== Bash Command Tests ===")
                test_bash_command(context, td)
                print("✅ Bash command tests passed")
                
                print("\n=== File Operations Tests ===")
                test_file_operations(context, td)
                print("✅ File operations tests passed")
                
                print("\n=== Nested Paths Tests ===")
                test_nested_paths(context, td)
                print("✅ Nested paths tests passed")
                
                print("\n=== All Tests Passed ===")
                
            finally:
                # Cleanup
                try:
                    bash_state.sendintr()
                    bash_state.reset_shell()
                    bash_state.cleanup()
                except Exception as e:
                    print(f"Error during cleanup: {e}")