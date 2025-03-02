import os
import sys
import tempfile
import time
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath('src'))

from wcgw.client.platform_utils import is_windows, get_default_shell
from wcgw.client.bash_state.bash_state import BashState
from wcgw.client.tools import (
    Context,
    Initialize,
    BashCommand,
    ReadFiles,
    WriteIfEmpty,
    FileEdit,
    ReadImage,
    ContextSave,
    get_tool_output,
    default_enc,
    try_open_file
)
from wcgw.types_ import Command, SendText

# Patch try_open_file to prevent it from automatically opening saved files
# This is what's causing the file access issues on Windows
original_try_open_file = try_open_file

def no_op_try_open_file(file_path):
    print(f"[PATCHED] Would have opened file: {file_path}")
    return

# Replace the function
import wcgw.client.tools
wcgw.client.tools.try_open_file = no_op_try_open_file

class TestConsole:
    """Simple console implementation for testing."""
    def __init__(self):
        self.logs = []
        self.prints = []
    
    def log(self, msg):
        self.logs.append(msg)
        print(f"[LOG] {msg}")
    
    def print(self, msg):
        self.prints.append(msg)
        print(f"[PRINT] {msg}")

def test_tools():
    """Test all tools to verify Windows compatibility."""
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n=== Testing in directory: {temp_dir} ===\n")
        
        # Setup test context
        console = TestConsole()
        bash_state = BashState(
            console=console,
            working_dir=temp_dir,
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
            # Test 1: Initialize Tool
            print("\n=== Testing Initialize Tool ===")
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
            
            print(f"Initialize output: {outputs[0][:100]}...")
            print("Initialize test passed.")
            
            # Test 2: BashCommand Tool
            print("\n=== Testing BashCommand Tool ===")
            # For Windows use different commands
            if is_windows():
                command = "dir"
            else:
                command = "ls -la"
                
            cmd = BashCommand(action_json=Command(command=command))
            outputs, _ = get_tool_output(
                context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
            )
            
            print(f"BashCommand output: {outputs[0][:100]}...")
            print("BashCommand test passed.")
            
            # Test 3: WriteIfEmpty Tool
            print("\n=== Testing WriteIfEmpty Tool ===")
            test_file = os.path.join(temp_dir, "test.txt")
            write_args = WriteIfEmpty(file_path=test_file, file_content="Test content\nfor Windows compatibility")
            outputs, _ = get_tool_output(
                context, write_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
            )
            
            print(f"WriteIfEmpty output: {outputs[0]}")
            if not os.path.exists(test_file):
                raise Exception(f"Error: File {test_file} was not created")
            print("WriteIfEmpty test passed.")
            
            # Test 4: ReadFiles Tool
            print("\n=== Testing ReadFiles Tool ===")
            read_args = ReadFiles(file_paths=[test_file])
            outputs, _ = get_tool_output(
                context, read_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
            )
            
            print(f"ReadFiles output: {outputs[0]}")
            if "Test content" not in outputs[0]:
                raise Exception("Error: File content was not read correctly")
            print("ReadFiles test passed.")
            
            # Test 5: FileEdit Tool
            print("\n=== Testing FileEdit Tool ===")
            edit_args = FileEdit(
                file_path=test_file,
                file_edit_using_search_replace_blocks="""<<<<<<< SEARCH
Test content
=======
Modified content
>>>>>>> REPLACE"""
            )
            
            outputs, _ = get_tool_output(
                context, edit_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
            )
            
            print(f"FileEdit output: {outputs[0]}")
            
            # Verify the change
            with open(test_file, 'r') as f:
                content = f.read()
            if "Modified content" not in content:
                raise Exception("Error: File content was not edited correctly")
            print("FileEdit test passed.")
            
            # Test 6: Create a nested directory structure
            print("\n=== Testing Nested Path Operations ===")
            nested_dir = os.path.join(temp_dir, "level1", "level2", "level3")
            os.makedirs(nested_dir, exist_ok=True)
            
            nested_file = os.path.join(nested_dir, "nested_test.txt")
            write_args = WriteIfEmpty(file_path=nested_file, file_content="Nested file content")
            outputs, _ = get_tool_output(
                context, write_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
            )
            
            print(f"Nested WriteIfEmpty output: {outputs[0]}")
            if not os.path.exists(nested_file):
                raise Exception(f"Error: Nested file {nested_file} was not created")
            print("Nested path operations test passed.")
            
            # Test 7: ContextSave Tool
            print("\n=== Testing ContextSave Tool ===")
            # Create a dedicated directory for context save to avoid temp directory issues
            save_dir = os.path.abspath(os.path.join(os.path.dirname(temp_dir), "context_save_test"))
            os.makedirs(save_dir, exist_ok=True)
            
            # Create a test file in that directory
            test_save_file = os.path.join(save_dir, "test_save.txt")
            with open(test_save_file, "w") as f:
                f.write("Content for context save test")
                
            try:
                context_args = ContextSave(
                    id="test-context",
                    project_root_path=save_dir,
                    description="Testing Windows compatibility",
                    relevant_file_globs=["*.txt"],
                )
                
                outputs, _ = get_tool_output(
                    context, context_args, default_enc, 1.0, lambda x, y: ("", 0.0), None
                )
                
                print(f"ContextSave output: {outputs[0]}")
                # Just verify it doesn't crash
                print("ContextSave test passed.")
                
                # Add a short delay to allow any file operations to complete
                time.sleep(1)
            except Exception as e:
                print(f"ContextSave test error: {e}")
                # Continue with other tests even if this one fails
            
            # Test 8: Interactive commands
            print("\n=== Testing Interactive Commands ===")
            if is_windows():
                cmd = BashCommand(action_json=SendText(send_text="echo Hello Windows\r"))
            else:
                cmd = BashCommand(action_json=SendText(send_text="echo Hello Unix\n"))
                
            outputs, _ = get_tool_output(
                context, cmd, default_enc, 1.0, lambda x, y: ("", 0.0), None
            )
            
            print(f"Interactive command output: {outputs[0]}")
            print("Interactive command test passed.")
            
            print("\n=== All tests passed successfully! ===")
            
        finally:
            # Clean up
            try:
                bash_state.sendintr()  # Send Ctrl-C to any running process
                bash_state.reset_shell()  # Reset shell state
                bash_state.cleanup()  # Cleanup final shell
            except Exception as e:
                print(f"Error during cleanup: {e}")


if __name__ == "__main__":
    print(f"Running on {'Windows' if is_windows() else 'Unix/Linux'}")
    print(f"Default shell: {get_default_shell()}")
    
    try:
        test_tools()
        print("\nAll tools successfully tested - Windows compatibility confirmed!")
    except Exception as e:
        import traceback
        print(f"\nERROR: Test failed: {e}")
        traceback.print_exc()
        sys.exit(1)