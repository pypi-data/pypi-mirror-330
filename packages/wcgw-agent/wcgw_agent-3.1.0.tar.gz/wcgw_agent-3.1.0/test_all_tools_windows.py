"""
WCGW Windows Compatibility Test - Tool-by-Tool Verification

This script systematically tests each tool in the WCGW toolkit for Windows compatibility.
It follows the same structure as test_tools.py but is optimized for Windows testing.
"""

import os
import sys
import time
import platform
import tempfile
from typing import Generator

# Add the src directory to Python path
sys.path.insert(0, os.path.abspath('src'))

# Try importing the necessary modules
try:
    from wcgw.client.bash_state.bash_state import BashState
    from wcgw.client.tools import (
        BashCommand,
        Context,
        ContextSave,
        Initialize,
        ReadFiles,
        ReadImage,
        WriteIfEmpty,
        FileEdit,
        default_enc,
        get_tool_output,
        which_tool_name,
    )
    from wcgw.types_ import (
        Command,
        Console,
        SendAscii,
        SendSpecials,
        SendText,
        StatusCheck,
    )
    from wcgw.client.platform_utils import (
        is_windows,
        is_mac,
        is_unix_like,
        get_default_shell,
        get_shell_launch_args,
        get_prompt_string
    )
    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    print(f"Error importing modules: {e}")
    IMPORTS_SUCCESSFUL = False

# Define a console class for testing
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

def create_test_context(working_dir):
    """Create a test context with the given working directory."""
    print(f"\nCreating test context with working directory: {working_dir}")
    console = TestConsole()
    try:
        bash_state = BashState(
            console=console,
            working_dir=working_dir,
            bash_command_mode=None,
            file_edit_mode=None,
            write_if_empty_mode=None,
            mode=None,
            use_screen=True,
        )
        ctx = Context(
            bash_state=bash_state,
            console=console,
        )
        return ctx, console
    except Exception as e:
        print(f"Error creating context: {e}")
        return None, console


def test_initialize_tool(working_dir):
    """Test the Initialize tool."""
    print("\n=== Testing Initialize Tool ===")
    ctx, console = create_test_context(working_dir)
    if not ctx:
        print("❌ Could not create context")
        return False
    
    try:
        # Test default wcgw mode
        init_args = Initialize(
            type="first_call",
            any_workspace_path=working_dir,
            initial_files_to_read=[],
            task_id_to_resume="",
            mode_name="wcgw",
            code_writer_config=None,
        )

        outputs, _ = get_tool_output(
            ctx, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )

        if len(outputs) == 1 and isinstance(outputs[0], str) and working_dir in outputs[0] and "System:" in outputs[0]:
            print("✅ Initialize tool test PASSED")
            return True
        else:
            print("❌ Initialize tool test FAILED")
            return False
    except Exception as e:
        print(f"❌ Error testing Initialize tool: {e}")
        return False
    finally:
        try:
            ctx.bash_state.cleanup()
        except Exception as e:
            print(f"Error during cleanup: {e}")


def test_bash_command_tool(working_dir):
    """Test the BashCommand tool."""
    print("\n=== Testing BashCommand Tool ===")
    ctx, console = create_test_context(working_dir)
    if not ctx:
        print("❌ Could not create context")
        return False
    
    try:
        # First initialize
        init_args = Initialize(
            type="first_call",
            any_workspace_path=working_dir,
            initial_files_to_read=[],
            task_id_to_resume="",
            mode_name="wcgw",
            code_writer_config=None,
        )
        get_tool_output(ctx, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None)
        
        # Test echo command
        print("Testing echo command...")
        cmd = BashCommand(action_json=Command(command='echo "hello world"'))
        outputs, _ = get_tool_output(
            ctx, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        echo_success = len(outputs) == 1 and "hello world" in outputs[0]
        print(f"Echo command test: {'✅ PASSED' if echo_success else '❌ FAILED'}")
        
        # Test status check
        print("Testing status check...")
        cmd = BashCommand(action_json=StatusCheck(status_check=True))
        outputs, _ = get_tool_output(
            ctx, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        status_check_success = "No running command to check status of" in outputs[0]
        print(f"Status check test: {'✅ PASSED' if status_check_success else '❌ FAILED'}")
        
        # Test long-running command
        print("Testing long-running command...")
        cmd = BashCommand(action_json=Command(command="timeout /t 2"), wait_for_seconds=0.1)
        outputs, _ = get_tool_output(
            ctx, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        long_running_success = "status = still running" in outputs[0]
        print(f"Long-running command test: {'✅ PASSED' if long_running_success else '❌ FAILED'}")
        
        # Test sending text
        print("Testing text input...")
        cmd = BashCommand(action_json=SendText(send_text="dir"))
        outputs, _ = get_tool_output(
            ctx, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        text_input_success = len(outputs) == 1
        print(f"Text input test: {'✅ PASSED' if text_input_success else '❌ FAILED'}")
        
        # Test sending Enter key
        print("Testing special keys...")
        cmd = BashCommand(action_json=SendSpecials(send_specials=["Enter"]))
        outputs, _ = get_tool_output(
            ctx, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        special_keys_success = len(outputs) == 1 and "Volume" in outputs[0]
        print(f"Special keys test: {'✅ PASSED' if special_keys_success else '❌ FAILED'}")
        
        # Test ASCII input
        print("Testing ASCII input...")
        cmd = BashCommand(action_json=SendAscii(send_ascii=[68, 73, 82]))  # "DIR"
        outputs, _ = get_tool_output(
            ctx, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        ascii_input_success = len(outputs) == 1
        print(f"ASCII input test: {'✅ PASSED' if ascii_input_success else '❌ FAILED'}")
        
        # Test Ctrl-C
        print("Testing Ctrl-C...")
        cmd = BashCommand(action_json=Command(command="timeout /t 5"), wait_for_seconds=0.1)
        outputs, _ = get_tool_output(
            ctx, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        cmd = BashCommand(action_json=SendSpecials(send_specials=["Ctrl-c"]))
        outputs, _ = get_tool_output(
            ctx, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        ctrl_c_success = "status = process exited" in outputs[0]
        print(f"Ctrl-C test: {'✅ PASSED' if ctrl_c_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = (echo_success and status_check_success and long_running_success 
                           and text_input_success and special_keys_success 
                           and ascii_input_success and ctrl_c_success)
        
        print(f"\nOverall BashCommand tool test: {'✅ PASSED' if overall_success else '❌ FAILED'}")
        return overall_success
    except Exception as e:
        print(f"❌ Error testing BashCommand tool: {e}")
        return False
    finally:
        try:
            ctx.bash_state.cleanup()
        except Exception as e:
            print(f"Error during cleanup: {e}")


def test_file_operations_tools(working_dir):
    """Test the WriteIfEmpty and ReadFiles tools."""
    print("\n=== Testing File Operations Tools ===")
    ctx, console = create_test_context(working_dir)
    if not ctx:
        print("❌ Could not create context")
        return False
    
    try:
        # First initialize
        init_args = Initialize(
            type="first_call",
            any_workspace_path=working_dir,
            initial_files_to_read=[],
            task_id_to_resume="",
            mode_name="wcgw",
            code_writer_config=None,
        )
        get_tool_output(ctx, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None)
        
        # Test WriteIfEmpty
        print("Testing WriteIfEmpty...")
        test_file = os.path.join(working_dir, "test.txt")
        write_args = WriteIfEmpty(file_path=test_file, file_content="test content\r\n")
        outputs, _ = get_tool_output(
            ctx, write_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        write_success = len(outputs) == 1 and "Success" in outputs[0]
        print(f"WriteIfEmpty test: {'✅ PASSED' if write_success else '❌ FAILED'}")
        
        # Test ReadFiles
        print("Testing ReadFiles...")
        read_args = ReadFiles(file_paths=[test_file])
        outputs, _ = get_tool_output(
            ctx, read_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        read_success = len(outputs) == 1 and "test content" in outputs[0]
        print(f"ReadFiles test: {'✅ PASSED' if read_success else '❌ FAILED'}")
        
        # Test writing to existing file without reading first
        print("Testing write to existing file without reading...")
        test_file2 = os.path.join(working_dir, "test2.txt")
        with open(test_file2, "w") as f:
            f.write("existing content\r\n")
            
        write_args = WriteIfEmpty(file_path=test_file2, file_content="new content\r\n")
        outputs, _ = get_tool_output(
            ctx, write_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        write_existing_success = len(outputs) == 1 and "Error: can't write to existing file" in outputs[0]
        print(f"WriteIfEmpty to existing file test: {'✅ PASSED' if write_existing_success else '❌ FAILED'}")
        
        # Test writing after reading
        print("Testing write after reading...")
        read_args = ReadFiles(file_paths=[test_file2])
        outputs, _ = get_tool_output(
            ctx, read_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        write_args = WriteIfEmpty(file_path=test_file2, file_content="new content after read\r\n")
        outputs, _ = get_tool_output(
            ctx, write_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        write_after_read_success = len(outputs) == 1 and "Warning: a file already existed" in outputs[0] and "Success" in outputs[0]
        print(f"WriteIfEmpty after reading test: {'✅ PASSED' if write_after_read_success else '❌ FAILED'}")
        
        # Test writing to nested directory
        print("Testing write to nested directory...")
        nested_dir = os.path.join(working_dir, "nested", "path")
        nested_file = os.path.join(nested_dir, "nested.txt")
        
        write_args = WriteIfEmpty(file_path=nested_file, file_content="nested content\r\n")
        outputs, _ = get_tool_output(
            ctx, write_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        nested_write_success = len(outputs) == 1 and "Success" in outputs[0]
        nested_dir_exists = os.path.exists(nested_dir)
        nested_file_exists = os.path.exists(nested_file)
        
        print(f"WriteIfEmpty to nested directory test: {'✅ PASSED' if nested_write_success and nested_dir_exists and nested_file_exists else '❌ FAILED'}")
        
        # Overall success
        overall_success = write_success and read_success and write_existing_success and write_after_read_success and nested_write_success
        
        print(f"\nOverall File Operations tools test: {'✅ PASSED' if overall_success else '❌ FAILED'}")
        return overall_success
    except Exception as e:
        print(f"❌ Error testing File Operations tools: {e}")
        return False
    finally:
        try:
            ctx.bash_state.cleanup()
        except Exception as e:
            print(f"Error during cleanup: {e}")


def test_file_edit_tool(working_dir):
    """Test the FileEdit tool."""
    print("\n=== Testing FileEdit Tool ===")
    ctx, console = create_test_context(working_dir)
    if not ctx:
        print("❌ Could not create context")
        return False
    
    try:
        # First initialize
        init_args = Initialize(
            type="first_call",
            any_workspace_path=working_dir,
            initial_files_to_read=[],
            task_id_to_resume="",
            mode_name="wcgw",
            code_writer_config=None,
        )
        get_tool_output(ctx, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None)
        
        # Create a test file
        test_file = os.path.join(working_dir, "code.py")
        with open(test_file, "w") as f:
            f.write("def hello():\r\n    print('hello')\r\n")
        
        # Test editing the file
        print("Testing FileEdit...")
        edit_args = FileEdit(
            file_path=test_file,
            file_edit_using_search_replace_blocks="""<<<<<<< SEARCH
def hello():
    print('hello')
=======
def hello():
    print('hello world')
>>>>>>> REPLACE""",
        )
        
        outputs, _ = get_tool_output(
            ctx, edit_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        edit_success = len(outputs) == 1
        
        # Verify the change
        with open(test_file, "r") as f:
            content = f.read()
        
        content_success = "hello world" in content
        print(f"FileEdit test: {'✅ PASSED' if edit_success and content_success else '❌ FAILED'}")
        
        # Test indentation matching
        print("Testing indentation matching...")
        edit_args = FileEdit(
            file_path=test_file,
            file_edit_using_search_replace_blocks="""<<<<<<< SEARCH
  def hello():
    print('hello world')     
=======
def hello():
    print('ok')
>>>>>>> REPLACE""",
        )
        
        outputs, _ = get_tool_output(
            ctx, edit_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        indentation_success = len(outputs) == 1 and "Warning: matching without considering indentation" in outputs[0]
        
        # Verify the change
        with open(test_file, "r") as f:
            content = f.read()
        
        indentation_content_success = "print('ok')" in content
        print(f"Indentation matching test: {'✅ PASSED' if indentation_success and indentation_content_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = edit_success and content_success and indentation_success and indentation_content_success
        
        print(f"\nOverall FileEdit tool test: {'✅ PASSED' if overall_success else '❌ FAILED'}")
        return overall_success
    except Exception as e:
        print(f"❌ Error testing FileEdit tool: {e}")
        return False
    finally:
        try:
            ctx.bash_state.cleanup()
        except Exception as e:
            print(f"Error during cleanup: {e}")


def test_context_save_tool(working_dir):
    """Test the ContextSave tool."""
    print("\n=== Testing ContextSave Tool ===")
    ctx, console = create_test_context(working_dir)
    if not ctx:
        print("❌ Could not create context")
        return False
    
    try:
        # First initialize
        init_args = Initialize(
            type="first_call",
            any_workspace_path=working_dir,
            initial_files_to_read=[],
            task_id_to_resume="",
            mode_name="wcgw",
            code_writer_config=None,
        )
        get_tool_output(ctx, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None)
        
        # Create test files
        test_file1 = os.path.join(working_dir, "test1.txt")
        test_file2 = os.path.join(working_dir, "test2.txt")
        
        with open(test_file1, "w") as f:
            f.write("test content 1")
        with open(test_file2, "w") as f:
            f.write("test content 2")
        
        # Test saving context
        print("Testing ContextSave...")
        save_args = ContextSave(
            id="test_save",
            project_root_path=working_dir,
            description="Test save",
            relevant_file_globs=["*.txt"],
        )
        
        outputs, _ = get_tool_output(
            ctx, save_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        save_success = len(outputs) == 1 and isinstance(outputs[0], str) and outputs[0].endswith(".txt")
        print(f"ContextSave test: {'✅ PASSED' if save_success else '❌ FAILED'}")
        
        # Test resuming context
        print("Testing context resumption...")
        init_args = Initialize(
            type="first_call",
            any_workspace_path=working_dir,
            initial_files_to_read=[],
            task_id_to_resume="test_save",
            mode_name="wcgw",
            code_writer_config=None,
        )
        
        outputs, _ = get_tool_output(
            ctx, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
        )
        
        resume_success = len(outputs) == 1 and "Following is the retrieved" in outputs[0]
        print(f"Context resumption test: {'✅ PASSED' if resume_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = save_success and resume_success
        
        print(f"\nOverall ContextSave tool test: {'✅ PASSED' if overall_success else '❌ FAILED'}")
        return overall_success
    except Exception as e:
        print(f"❌ Error testing ContextSave tool: {e}")
        return False
    finally:
        try:
            ctx.bash_state.cleanup()
        except Exception as e:
            print(f"Error during cleanup: {e}")


def test_read_image_tool(working_dir):
    """Test the ReadImage tool."""
    print("\n=== Testing ReadImage Tool ===")
    ctx, console = create_test_context(working_dir)
    if not ctx:
        print("❌ Could not create context")
        return False
    
    try:
        # First initialize
        init_args = Initialize(
            type="first_call",
            any_workspace_path=working_dir,
            initial_files_to_read=[],
            task_id_to_resume="",
            mode_name="wcgw",
            code_writer_config=None,
        )
        get_tool_output(ctx, init_args, default_enc, 1.0, lambda x, y: ("", 0.0), None)
        
        # Create a small test image
        test_image = os.path.join(working_dir, "test.png")
        try:
            # Write a minimal valid PNG file
            with open(test_image, "wb") as f:
                f.write(
                    bytes.fromhex(
                        "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d4944415478da63640000000600005c0010ef0000000049454e44ae426082"
                    )
                )
            
            # Test reading image
            print("Testing ReadImage...")
            read_args = ReadImage(file_path=test_image)
            outputs, _ = get_tool_output(
                ctx, read_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
            )
            
            image_success = (len(outputs) == 1 and 
                            hasattr(outputs[0], "media_type") and 
                            outputs[0].media_type == "image/png" and
                            hasattr(outputs[0], "data"))
            
            print(f"ReadImage test: {'✅ PASSED' if image_success else '❌ FAILED'}")
            return image_success
        except Exception as e:
            print(f"❌ Error creating or reading test image: {e}")
            return False
    except Exception as e:
        print(f"❌ Error testing ReadImage tool: {e}")
        return False
    finally:
        try:
            ctx.bash_state.cleanup()
        except Exception as e:
            print(f"Error during cleanup: {e}")


def main():
    """Main function to run all tool tests."""
    print("======================================")
    print("WCGW Windows Compatibility Test Suite")
    print("Tool-by-Tool Verification")
    print("======================================")
    
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python version: {sys.version}")
    
    if not IMPORTS_SUCCESSFUL:
        print("\n❌ Module imports failed. Cannot proceed with tests.")
        return False
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\nTemporary test directory: {temp_dir}")
        
        # Run all tool tests
        results = {
            "Initialize Tool": test_initialize_tool(temp_dir),
            "BashCommand Tool": test_bash_command_tool(temp_dir),
            "File Operations Tools": test_file_operations_tools(temp_dir),
            "FileEdit Tool": test_file_edit_tool(temp_dir),
            "ContextSave Tool": test_context_save_tool(temp_dir),
            "ReadImage Tool": test_read_image_tool(temp_dir),
        }
        
        # Print summary
        print("\n======================================")
        print("Test Results Summary")
        print("======================================")
        
        passed = 0
        failed = 0
        
        for test_name, result in results.items():
            status = "PASSED" if result else "FAILED"
            status_symbol = "✅" if result else "❌"
            print(f"{status_symbol} {test_name}: {status}")
            
            if result:
                passed += 1
            else:
                failed += 1
        
        print(f"\nTools Tested: {len(results)}")
        print(f"Tools Passed: {passed}")
        print(f"Tools Failed: {failed}")
        
        if failed == 0:
            print("\n✅ ALL TOOLS PASSED - Windows compatibility confirmed!")
            return True
        else:
            print(f"\n❌ {failed} TOOLS FAILED - Windows compatibility issues detected!")
            return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)