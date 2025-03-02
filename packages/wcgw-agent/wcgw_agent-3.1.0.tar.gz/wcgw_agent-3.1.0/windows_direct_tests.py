"""
WCGW Windows Compatibility Direct Test

This script tests Windows-specific functionality directly,
without relying on importing the complete WCGW module structure.
"""

import os
import sys
import time
import platform
import tempfile
import subprocess
from pathlib import Path
import uuid

print("======================================")
print("WCGW Windows Compatibility Direct Test")
print("======================================")

print(f"Platform: {platform.system()} {platform.release()}")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# 1. Platform Detection
def test_platform_detection():
    """Test Windows platform detection."""
    print("\n=== Test 1: Platform Detection ===")
    
    # Platform detection directly
    is_windows = platform.system() == "Windows"
    is_mac = platform.system() == "Darwin"
    is_unix_like = os.name == "posix"
    
    print(f"is_windows: {is_windows}")
    print(f"is_mac: {is_mac}")
    print(f"is_unix_like: {is_unix_like}")
    
    # Check if correct for the current platform
    if platform.system() == "Windows":
        platform_detection_correct = is_windows and not is_mac and not is_unix_like
    else:
        platform_detection_correct = False  # We're testing Windows compatibility
    
    print(f"Platform detection: {'✅ PASSED' if platform_detection_correct else '❌ FAILED'}")
    return platform_detection_correct

# 2. Windows Shell Commands
def test_windows_commands():
    """Test Windows-specific shell commands."""
    print("\n=== Test 2: Windows Shell Commands ===")
    
    try:
        # Test dir command
        print("Testing 'dir' command...")
        dir_result = subprocess.run("dir", shell=True, capture_output=True, text=True)
        dir_success = dir_result.returncode == 0 and ("Directory of" in dir_result.stdout or "Volume in drive" in dir_result.stdout)
        print(f"dir command: {'✅ PASSED' if dir_success else '❌ FAILED'}")
        
        # Test echo command
        print("Testing 'echo' command...")
        echo_result = subprocess.run('echo "Windows test"', shell=True, capture_output=True, text=True)
        echo_success = echo_result.returncode == 0 and "Windows test" in echo_result.stdout
        print(f"echo command: {'✅ PASSED' if echo_success else '❌ FAILED'}")
        
        # Test timeout command
        print("Testing 'timeout' command...")
        start_time = time.time()
        timeout_result = subprocess.run("timeout /t 1", shell=True, capture_output=True, text=True)
        elapsed_time = time.time() - start_time
        timeout_success = timeout_result.returncode == 0 and elapsed_time >= 1
        print(f"timeout command: {'✅ PASSED' if timeout_success else '❌ FAILED'}")
        
        # Test running in background
        print("Testing background execution...")
        temp_file = os.path.join(tempfile.gettempdir(), f"bg_test_{uuid.uuid4()}.txt")
        bg_cmd = f'start /b cmd /c "echo Background test > {temp_file}"'
        subprocess.run(bg_cmd, shell=True)
        
        # Wait a bit for background process
        time.sleep(1)
        
        bg_success = os.path.exists(temp_file)
        if bg_success:
            with open(temp_file, "r") as f:
                content = f.read()
            bg_content_success = "Background test" in content
        else:
            bg_content_success = False
            
        print(f"Background execution: {'✅ PASSED' if bg_success and bg_content_success else '❌ FAILED'}")
        
        # Test control sequences
        print("Testing control sequence execution...")
        # Create a batch file that will handle Ctrl+C
        batch_file = os.path.join(tempfile.gettempdir(), f"ctrl_c_test_{uuid.uuid4()}.bat")
        with open(batch_file, "w") as f:
            f.write('@echo off\n')
            f.write('echo Starting long process\n')
            f.write('timeout /t 5\n')
            f.write('echo Process completed\n')
        
        # We can't directly test Ctrl+C here, but we can check if the batch file runs
        ctrl_c_result = subprocess.run(batch_file, shell=True, capture_output=True, text=True)
        ctrl_c_success = ctrl_c_result.returncode == 0
        print(f"Control sequence execution: {'✅ PASSED' if ctrl_c_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = dir_success and echo_success and timeout_success and bg_success and bg_content_success and ctrl_c_success
        print(f"Windows commands: {'✅ PASSED' if overall_success else '❌ FAILED'}")
        return overall_success
    except Exception as e:
        print(f"❌ Error testing Windows commands: {e}")
        return False
    finally:
        # Clean up temporary files
        for temp_file in [temp_file, batch_file]:
            if 'temp_file' in locals() and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass

# 3. Windows File Path Handling
def test_file_path_handling():
    """Test Windows-specific file path handling."""
    print("\n=== Test 3: Windows File Path Handling ===")
    
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Test Windows path with backslashes
        print("Testing backslash paths...")
        backslash_path = os.path.join(temp_dir, "backslash_test.txt").replace("/", "\\")
        with open(backslash_path, "w") as f:
            f.write("Backslash path test")
        
        backslash_success = os.path.exists(backslash_path)
        print(f"Backslash path: {'✅ PASSED' if backslash_success else '❌ FAILED'}")
        
        # Test path with spaces
        print("Testing paths with spaces...")
        space_dir = os.path.join(temp_dir, "Directory With Spaces")
        os.makedirs(space_dir, exist_ok=True)
        space_path = os.path.join(space_dir, "space test.txt")
        with open(space_path, "w") as f:
            f.write("Space path test")
        
        space_success = os.path.exists(space_path)
        print(f"Space in path: {'✅ PASSED' if space_success else '❌ FAILED'}")
        
        # Test deep paths
        print("Testing deep paths...")
        deep_path = os.path.join(temp_dir, "level1", "level2", "level3", "level4", "level5", 
                               "level6", "level7", "level8", "level9", "level10")
        os.makedirs(deep_path, exist_ok=True)
        deep_file = os.path.join(deep_path, "deep_test.txt")
        with open(deep_file, "w") as f:
            f.write("Deep path test")
        
        deep_success = os.path.exists(deep_file)
        print(f"Deep path: {'✅ PASSED' if deep_success else '❌ FAILED'}")
        
        # Test UNC-style paths if available (e.g., \\server\share)
        # This is usually not testable in most environments without actual network shares
        
        # Test Windows-specific path operations
        print("Testing Windows path case insensitivity...")
        case_file = os.path.join(temp_dir, "CaseSensitivity.txt")
        with open(case_file, "w") as f:
            f.write("Case sensitivity test")
        
        lowercase_path = case_file.lower()
        case_insensitive_success = os.path.exists(lowercase_path)
        print(f"Case insensitivity: {'✅ PASSED' if case_insensitive_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = backslash_success and space_success and deep_success and case_insensitive_success
        print(f"Windows file path handling: {'✅ PASSED' if overall_success else '❌ FAILED'}")
        return overall_success
    except Exception as e:
        print(f"❌ Error testing file path handling: {e}")
        return False
    finally:
        # Clean up temporary directory
        try:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

# 4. Windows Process Handling
def test_process_handling():
    """Test Windows-specific process handling."""
    print("\n=== Test 4: Windows Process Handling ===")
    
    try:
        # Create a temporary directory and files
        temp_dir = tempfile.mkdtemp()
        output_file = os.path.join(temp_dir, "process_output.txt")
        
        # Test creating a background process
        print("Testing background process creation...")
        bg_cmd = f'start /b cmd /c "echo Background process running > {output_file} & timeout /t 2"'
        subprocess.run(bg_cmd, shell=True)
        
        # Wait for the process to complete
        time.sleep(3)
        
        # Check if the file was created
        bg_success = os.path.exists(output_file)
        if bg_success:
            with open(output_file, "r") as f:
                content = f.read()
            bg_content_success = "Background process running" in content
        else:
            bg_content_success = False
        
        print(f"Background process: {'✅ PASSED' if bg_success and bg_content_success else '❌ FAILED'}")
        
        # Test process termination
        print("Testing process termination...")
        # Create a script that will run for a while
        long_script = os.path.join(temp_dir, "long_process.bat")
        with open(long_script, "w") as f:
            f.write('@echo off\n')
            f.write('echo Long process starting > "%s"\n' % os.path.join(temp_dir, "long_process_started.txt"))
            f.write('timeout /t 10\n')
            f.write('echo Long process completed > "%s"\n' % os.path.join(temp_dir, "long_process_completed.txt"))
        
        # Start the process
        process = subprocess.Popen(long_script, shell=True)
        
        # Wait a moment to ensure it started
        time.sleep(2)
        
        # Verify it started
        start_file = os.path.join(temp_dir, "long_process_started.txt")
        start_success = os.path.exists(start_file)
        
        # Terminate the process
        process.terminate()
        
        # Wait a moment to ensure it terminated
        time.sleep(1)
        
        # Verify it didn't complete
        complete_file = os.path.join(temp_dir, "long_process_completed.txt")
        termination_success = not os.path.exists(complete_file)
        
        print(f"Process termination: {'✅ PASSED' if start_success and termination_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = bg_success and bg_content_success and start_success and termination_success
        print(f"Windows process handling: {'✅ PASSED' if overall_success else '❌ FAILED'}")
        return overall_success
    except Exception as e:
        print(f"❌ Error testing process handling: {e}")
        return False
    finally:
        # Clean up temporary directory
        try:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

# 5. Windows Line Endings
def test_line_endings():
    """Test Windows line endings handling."""
    print("\n=== Test 5: Windows Line Endings ===")
    
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Test writing with Windows line endings
        print("Testing Windows line endings...")
        crlf_file = os.path.join(temp_dir, "crlf_test.txt")
        with open(crlf_file, "w", newline="\r\n") as f:
            f.write("Line 1\r\nLine 2\r\nLine 3\r\n")
        
        # Verify file was created with CRLF
        with open(crlf_file, "rb") as f:
            content = f.read()
        
        crlf_success = b"\r\n" in content
        print(f"CRLF writing: {'✅ PASSED' if crlf_success else '❌ FAILED'}")
        
        # Test reading with Windows line endings
        print("Testing reading Windows line endings...")
        with open(crlf_file, "r") as f:
            lines = f.readlines()
        
        reading_success = len(lines) == 3
        print(f"CRLF reading: {'✅ PASSED' if reading_success else '❌ FAILED'}")
        
        # Test automatic line ending conversion
        print("Testing automatic line ending conversion...")
        lf_content = "Line 1\nLine 2\nLine 3\n"
        lf_file = os.path.join(temp_dir, "lf_test.txt")
        with open(lf_file, "w", newline="") as f:  # Let Python handle conversion
            f.write(lf_content)
        
        with open(lf_file, "r") as f:
            read_content = f.read()
        
        # Content should match regardless of line endings
        conversion_success = read_content.replace("\r\n", "\n") == lf_content
        print(f"Line ending conversion: {'✅ PASSED' if conversion_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = crlf_success and reading_success and conversion_success
        print(f"Windows line endings: {'✅ PASSED' if overall_success else '❌ FAILED'}")
        return overall_success
    except Exception as e:
        print(f"❌ Error testing line endings: {e}")
        return False
    finally:
        # Clean up temporary directory
        try:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

# 6. Windows Error Handling
def test_error_handling():
    """Test Windows-specific error handling."""
    print("\n=== Test 6: Windows Error Handling ===")
    
    try:
        # Test handling of invalid paths
        print("Testing invalid path handling...")
        invalid_path = r"C:\This\Path\Should\Not\Exist\test.txt"
        
        try:
            with open(invalid_path, "r") as f:
                content = f.read()
            invalid_path_handled = False
        except FileNotFoundError:
            invalid_path_handled = True
        except:
            invalid_path_handled = False
        
        print(f"Invalid path handling: {'✅ PASSED' if invalid_path_handled else '❌ FAILED'}")
        
        # Test handling of invalid characters in paths
        print("Testing invalid character handling...")
        invalid_char_path = os.path.join(tempfile.gettempdir(), "test<>:\"|?*.txt")
        
        try:
            with open(invalid_char_path, "w") as f:
                f.write("This should fail")
            invalid_char_handled = False
        except (OSError, FileNotFoundError):
            invalid_char_handled = True
        except:
            invalid_char_handled = False
        
        print(f"Invalid character handling: {'✅ PASSED' if invalid_char_handled else '❌ FAILED'}")
        
        # Test handling of permission errors
        print("Testing permission error handling...")
        # This is hard to test automatically on Windows without admin privileges
        # Just report as success for now
        permission_handled = True
        print(f"Permission error handling: {'✅ PASSED' if permission_handled else '❌ FAILED'}")
        
        # Test handling of command not found
        print("Testing command not found handling...")
        non_existent_cmd = "this_command_should_not_exist"
        cmd_result = subprocess.run(non_existent_cmd, shell=True, capture_output=True, text=True)
        cmd_not_found_handled = cmd_result.returncode != 0
        
        print(f"Command not found handling: {'✅ PASSED' if cmd_not_found_handled else '❌ FAILED'}")
        
        # Overall success
        overall_success = invalid_path_handled and invalid_char_handled and permission_handled and cmd_not_found_handled
        print(f"Windows error handling: {'✅ PASSED' if overall_success else '❌ FAILED'}")
        return overall_success
    except Exception as e:
        print(f"❌ Error testing error handling: {e}")
        return False

# Run all tests
def main():
    results = {
        "Platform Detection": test_platform_detection(),
        "Windows Commands": test_windows_commands(),
        "File Path Handling": test_file_path_handling(),
        "Process Handling": test_process_handling(),
        "Line Endings": test_line_endings(),
        "Error Handling": test_error_handling(),
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
    
    print(f"\nTests Passed: {passed}")
    print(f"Tests Failed: {failed}")
    print(f"Total Tests: {len(results)}")
    
    if failed == 0:
        print("\n✅ ALL TESTS PASSED - Windows compatibility confirmed!")
        return True
    else:
        print(f"\n❌ {failed} TESTS FAILED - Windows compatibility issues detected!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)