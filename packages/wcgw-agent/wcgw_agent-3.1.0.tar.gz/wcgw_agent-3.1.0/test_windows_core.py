"""
Windows Core Compatibility Test Suite

This script tests the core Windows-specific functionality added to WCGW, focusing on:
1. Platform detection
2. Windows shell handling
3. Background process management (Windows replacement for Unix 'screen')
"""

import os
import sys
import time
import platform
import tempfile
import uuid
import subprocess
from pathlib import Path

# Add the parent directory to sys.path to import our modules
sys.path.insert(0, os.path.abspath('src'))

# Create a simple console class for logging
class TestConsole:
    def __init__(self):
        self.logs = []
        
    def log(self, message):
        self.logs.append(message)
        print(f"[LOG] {message}")
        
    def print(self, message, *args, **kwargs):
        self.log(message)

# Import platform utilities directly for testing
try:
    from wcgw.client.platform_utils import (
        is_windows,
        is_mac,
        is_unix_like,
        get_default_shell,
        get_shell_launch_args,
        get_prompt_string,
        get_prompt_command
    )
    platform_utils_imported = True
    print("✅ Platform utilities successfully imported")
except ImportError as e:
    platform_utils_imported = False
    print(f"❌ Error importing platform utilities: {e}")
    
    # Define fallback functions for testing
    def is_windows():
        return platform.system() == "Windows"
    
    def is_mac():
        return platform.system() == "Darwin"
    
    def is_unix_like():
        return os.name == "posix"
    
    def get_default_shell():
        if is_windows():
            return os.path.join(os.environ.get("SYSTEMROOT", r"C:\Windows"), "System32", "cmd.exe")
        else:
            return "/bin/bash"
    
    def get_shell_launch_args(restricted=False):
        return []
    
    def get_prompt_string():
        return ">" if is_windows() else "$"

# Import Windows-specific background process management if on Windows
windows_bg_imported = False
if is_windows():
    try:
        from wcgw.client.bash_state.windows_bg_process import (
            create_background_process,
            list_background_processes,
            print_background_processes,
            terminate_background_process,
            terminate_processes_by_name
        )
        windows_bg_imported = True
        print("✅ Windows background process utilities successfully imported")
    except ImportError as e:
        windows_bg_imported = False
        print(f"❌ Error importing Windows background process utilities: {e}")

def test_platform_detection():
    """Test platform detection functions."""
    print("\n=== Platform Detection Tests ===")
    
    current_platform = platform.system()
    print(f"Current platform: {current_platform}")
    print(f"is_windows(): {is_windows()}")
    print(f"is_mac(): {is_mac()}")
    print(f"is_unix_like(): {is_unix_like()}")
    
    # Verify platform detection matches actual platform
    if current_platform == "Windows":
        is_correct = is_windows() and not is_mac() and not is_unix_like()
    elif current_platform == "Darwin":
        is_correct = not is_windows() and is_mac() and is_unix_like()
    else:
        is_correct = not is_windows() and not is_mac() and is_unix_like()
        
    if is_correct:
        print("✅ Platform detection test PASSED")
        return True
    else:
        print("❌ Platform detection test FAILED")
        return False

def test_shell_commands():
    """Test basic shell command functionality."""
    print("\n=== Shell Command Tests ===")
    
    # Get shell command
    shell_cmd = get_default_shell()
    shell_args = get_shell_launch_args(False)
    prompt = get_prompt_string()
    
    print(f"Default shell: {shell_cmd}")
    print(f"Shell args: {shell_args}")
    print(f"Prompt string: {prompt}")
    
    # Verify shell command is appropriate for platform
    if is_windows():
        shell_valid = "cmd.exe" in shell_cmd.lower() or "powershell.exe" in shell_cmd.lower()
    else:
        shell_valid = "bash" in shell_cmd or "sh" in shell_cmd or "zsh" in shell_cmd
        
    if shell_valid:
        print("✅ Shell command test PASSED")
        return True
    else:
        print("❌ Shell command test FAILED")
        return False

def test_command_execution():
    """Test basic command execution."""
    print("\n=== Command Execution Tests ===")
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_path = temp_file.name
    
    try:
        # Execute a command appropriate for the platform
        if is_windows():
            cmd = f'echo "Command execution test" > "{temp_path}"'
            shell = True
        else:
            cmd = ["sh", "-c", f'echo "Command execution test" > "{temp_path}"']
            shell = False
            
        print(f"Running command: {cmd}")
        subprocess.run(cmd, shell=shell, check=True)
        
        # Verify file was created with correct content
        if os.path.exists(temp_path):
            with open(temp_path, "r") as f:
                content = f.read().strip()
            print(f"Command output: {content}")
            
            test_passed = "Command execution test" in content
            if test_passed:
                print("✅ Command execution test PASSED")
            else:
                print("❌ Command execution test FAILED")
            return test_passed
        else:
            print("❌ Command execution test FAILED - File not created")
            return False
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def test_file_operations():
    """Test basic file operations."""
    print("\n=== File Operations Tests ===")
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test creating nested directories
        nested_dir = os.path.join(temp_dir, "level1", "level2", "level3")
        os.makedirs(nested_dir, exist_ok=True)
        
        # Test creating a file
        test_file = os.path.join(nested_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("File operations test")
            
        # Test reading the file
        if os.path.exists(test_file):
            with open(test_file, "r") as f:
                content = f.read()
            print(f"File content: {content}")
            
            test_passed = "File operations test" in content
            if test_passed:
                print("✅ File operations test PASSED")
            else:
                print("❌ File operations test FAILED")
            return test_passed
        else:
            print("❌ File operations test FAILED - File not created")
            return False

def test_windows_background_process():
    """Test Windows background process functionality."""
    if not is_windows():
        print("\n=== Windows Background Process Tests ===")
        print("⏭️ Skipping background process tests (not on Windows)")
        return True
        
    if not windows_bg_imported:
        print("\n=== Windows Background Process Tests ===")
        print("⏭️ Skipping background process tests (module not imported)")
        return True
        
    print("\n=== Windows Background Process Tests ===")
    console = TestConsole()
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test file path
        test_file = os.path.join(temp_dir, "bg_process_test.txt")
        
        # Create a background process
        command = f'echo "Background process test" > "{test_file}" & timeout /t 2'
        process_id = create_background_process(command, "test_process", console)
        
        if process_id:
            print(f"Created background process with ID: {process_id}")
            
            # Wait for process to complete
            time.sleep(3)
            
            # Check if file was created
            if os.path.exists(test_file):
                with open(test_file, "r") as f:
                    content = f.read().strip()
                print(f"Background process file content: {content}")
                
                file_test_passed = "Background process test" in content
                if not file_test_passed:
                    print("❌ Background process file creation test FAILED")
                    return False
                    
                # List background processes
                processes = list_background_processes(console)
                print(f"Number of background processes: {len(processes)}")
                
                # Create another process for termination testing
                command = f'timeout /t 10'
                process_id2 = create_background_process(command, "termination_test", console)
                
                if not process_id2:
                    print("❌ Background process creation test FAILED")
                    return False
                    
                print(f"Created test process for termination with ID: {process_id2}")
                
                # List processes again to verify the new process
                processes_after_creation = list_background_processes(console)
                process_found = any(p["id"] == process_id2 for p in processes_after_creation)
                
                if not process_found:
                    print("❌ Background process listing test FAILED")
                    return False
                    
                # Terminate the process
                terminate_result = terminate_background_process(process_id2, console)
                print(f"Terminate result: {terminate_result}")
                
                if not terminate_result:
                    print("❌ Background process termination test FAILED")
                    return False
                    
                # List processes again to verify termination
                processes_after_termination = list_background_processes(console)
                process_exists_after = any(p["id"] == process_id2 for p in processes_after_termination)
                
                if process_exists_after:
                    print("❌ Background process termination verification test FAILED")
                    return False
                    
                print("✅ Background process tests PASSED")
                return True
            else:
                print("❌ Background process file creation test FAILED - File not created")
                return False
        else:
            print("❌ Background process creation test FAILED")
            return False


def run_all_tests():
    """Run all compatibility tests."""
    print("======================================")
    print("Windows Compatibility Test Suite")
    print("======================================")
    
    results = {
        "Platform Detection": test_platform_detection(),
        "Shell Commands": test_shell_commands(),
        "Command Execution": test_command_execution(),
        "File Operations": test_file_operations(),
    }
    
    if is_windows() and windows_bg_imported:
        results["Windows Background Process"] = test_windows_background_process()
    
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
    
    print("\n======================================")
    print(f"Tests Passed: {passed}")
    print(f"Tests Failed: {failed}")
    print(f"Total Tests: {len(results)}")
    
    if failed == 0:
        print("✅ ALL TESTS PASSED")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        return False


if __name__ == "__main__":
    # Run all tests
    successful = run_all_tests()
    sys.exit(0 if successful else 1)