import os
import sys
import time
import platform
import subprocess
import tempfile
import uuid

print("=== Windows Compatibility Standalone Test ===")
print(f"Platform: {platform.system()} {platform.release()}")
print(f"Python: {sys.version}")

# Directly include the necessary functions from platform_utils.py
def is_windows():
    """Check if the current platform is Windows."""
    return platform.system() == "Windows"

def is_mac():
    """Check if the current platform is macOS."""
    return platform.system() == "Darwin"

def is_unix_like():
    """Check if the current platform is Unix-like (macOS, Linux, etc.)."""
    return os.name == "posix"

def get_default_shell():
    """Get the default shell for the current platform."""
    if is_windows():
        # On Windows, prefer PowerShell if available, otherwise use cmd.exe
        if os.path.exists(os.path.join(os.environ.get("SYSTEMROOT", r"C:\Windows"), "System32", "WindowsPowerShell", "v1.0", "powershell.exe")):
            return os.path.join(os.environ.get("SYSTEMROOT", r"C:\Windows"), "System32", "WindowsPowerShell", "v1.0", "powershell.exe")
        return os.path.join(os.environ.get("SYSTEMROOT", r"C:\Windows"), "System32", "cmd.exe")
    else:
        # On Unix-like systems, use the shell from the environment or default to /bin/bash
        return os.environ.get("SHELL", "/bin/bash")

# Directly include the necessary functions from windows_bg_process.py
def create_background_process(command, process_name, console):
    """Create a background process on Windows.
    
    Args:
        command: The command to execute
        process_name: A name for the process
        console: A console object with log method
        
    Returns:
        str: The process ID
    """
    if not is_windows():
        console.log("Not running on Windows, background process creation not supported")
        return None
        
    # Generate a unique ID for the process
    process_id = str(uuid.uuid4())
    
    # Create a temporary batch file to run the command
    batch_file = os.path.join(tempfile.gettempdir(), f"{process_id}.bat")
    
    with open(batch_file, "w") as f:
        f.write(f"@echo off\n{command}")
    
    # Start the process
    try:
        process = subprocess.Popen(
            ["cmd", "/c", batch_file],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        console.log(f"Started background process {process_id} for '{process_name}' with PID {process.pid}")
        
        # Store process information
        process_info = {
            "id": process_id,
            "name": process_name,
            "pid": process.pid,
            "process": process,
            "batch_file": batch_file,
            "start_time": time.time()
        }
        
        # Save process info to a temp file
        with open(os.path.join(tempfile.gettempdir(), f"{process_id}.json"), "w") as f:
            import json
            # Convert process to PID for JSON serialization
            process_info_json = process_info.copy()
            process_info_json["process"] = process.pid
            f.write(json.dumps(process_info_json))
        
        return process_id
    except Exception as e:
        console.log(f"Error starting background process: {e}")
        if os.path.exists(batch_file):
            os.unlink(batch_file)
        return None

def list_background_processes(console):
    """List all background processes.
    
    Args:
        console: A console object with log method
        
    Returns:
        list: A list of process information dictionaries
    """
    if not is_windows():
        console.log("Not running on Windows, background process listing not supported")
        return []
        
    processes = []
    temp_dir = tempfile.gettempdir()
    
    for filename in os.listdir(temp_dir):
        if filename.endswith(".json") and len(filename) > 5:
            try:
                process_id = filename[:-5]  # Remove .json
                json_path = os.path.join(temp_dir, filename)
                
                with open(json_path, "r") as f:
                    import json
                    process_info = json.loads(f.read())
                    
                # Skip if doesn't have required fields
                if not all(key in process_info for key in ["id", "name", "pid"]):
                    continue
                    
                # Check if process is still running
                try:
                    # Try to get process information using the PID
                    process = subprocess.Popen(
                        f"tasklist /FI \"PID eq {process_info['pid']}\" /FO CSV /NH",
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    output, _ = process.communicate()
                    
                    if str(process_info["pid"]) in output:
                        process_info["running"] = True
                    else:
                        process_info["running"] = False
                        
                    processes.append(process_info)
                except Exception as e:
                    console.log(f"Error checking process {process_id}: {e}")
                    
            except Exception as e:
                console.log(f"Error reading process file {filename}: {e}")
                
    return processes

def print_background_processes(console):
    """Print information about all background processes.
    
    Args:
        console: A console object with log method
    """
    processes = list_background_processes(console)
    
    if not processes:
        console.log("No background processes found")
        return
        
    console.log(f"Found {len(processes)} background processes:")
    for i, process in enumerate(processes):
        running_status = "RUNNING" if process.get("running", False) else "STOPPED"
        console.log(f"{i+1}. [{running_status}] {process['name']} (ID: {process['id']}, PID: {process['pid']})")

def terminate_background_process(process_id, console):
    """Terminate a background process.
    
    Args:
        process_id: The process ID to terminate
        console: A console object with log method
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not is_windows():
        console.log("Not running on Windows, background process termination not supported")
        return False
        
    temp_dir = tempfile.gettempdir()
    json_path = os.path.join(temp_dir, f"{process_id}.json")
    batch_path = os.path.join(temp_dir, f"{process_id}.bat")
    
    if not os.path.exists(json_path):
        console.log(f"Process {process_id} not found")
        return False
        
    try:
        # Load process information
        with open(json_path, "r") as f:
            import json
            process_info = json.loads(f.read())
            
        # Terminate the process
        try:
            subprocess.run(
                f"taskkill /F /PID {process_info['pid']}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            console.log(f"Terminated process {process_id} (PID: {process_info['pid']})")
        except Exception as e:
            console.log(f"Error terminating process: {e}")
            
        # Clean up files
        if os.path.exists(json_path):
            os.unlink(json_path)
            
        if os.path.exists(batch_path):
            os.unlink(batch_path)
            
        return True
    except Exception as e:
        console.log(f"Error terminating process {process_id}: {e}")
        return False

# Simple console class for logging
class SimpleConsole:
    def __init__(self):
        self.logs = []
        
    def log(self, message):
        self.logs.append(message)
        print(f"[LOG] {message}")
        
    def print(self, message, *args, **kwargs):
        self.log(message)

# Run tests
def run_tests():
    console = SimpleConsole()
    
    # Section 1: Platform Detection Tests
    print("\n=== Platform Detection Tests ===")
    print(f"is_windows(): {is_windows()}")
    print(f"is_mac(): {is_mac()}")
    print(f"is_unix_like(): {is_unix_like()}")
    print(f"Default shell: {get_default_shell()}")
    
    if not is_windows():
        print("Not running on Windows, skipping Windows-specific tests")
        return
    
    # Section 2: Background Process Tests
    print("\n=== Background Process Tests ===")
    
    # Test creating a background process
    print("\nTest 1: Creating background process")
    test_file = os.path.join(os.getcwd(), "bg_process_test.txt")
    if os.path.exists(test_file):
        os.unlink(test_file)
        
    command = f'echo "Background process test" > "{test_file}" & timeout /t 5'
    process_id = create_background_process(command, "test_process", console)
    
    if not process_id:
        print("Failed to create background process")
        return
        
    print(f"Created background process with ID: {process_id}")
    
    # Wait for file to be created
    time.sleep(2)
    
    # Check if file was created
    if os.path.exists(test_file):
        with open(test_file, "r") as f:
            content = f.read().strip()
        print(f"Background process file content: {content}")
        file_test_passed = "Background process test" in content
        print(f"File creation test: {'PASSED' if file_test_passed else 'FAILED'}")
    else:
        print("File creation test: FAILED - File was not created")
        file_test_passed = False
    
    # Test listing background processes
    print("\nTest 2: Listing background processes")
    processes = list_background_processes(console)
    print(f"Number of background processes: {len(processes)}")
    print_background_processes(console)
    
    # Verify our process is in the list
    process_found = any(p["id"] == process_id for p in processes)
    print(f"Process listing test: {'PASSED' if process_found else 'FAILED'}")
    
    # Test terminating the background process
    print("\nTest 3: Terminating background process")
    result = terminate_background_process(process_id, console)
    print(f"Termination result: {result}")
    
    # Wait a bit
    time.sleep(1)
    
    # Verify process was terminated
    processes_after = list_background_processes(console)
    process_exists_after = any(p["id"] == process_id for p in processes_after)
    print(f"Process termination test: {'PASSED' if not process_exists_after else 'FAILED'}")
    
    # Clean up test file
    if os.path.exists(test_file):
        os.unlink(test_file)
        print("Test file removed")
        
    # Overall test result
    overall_passed = file_test_passed and process_found and result and not process_exists_after
    print(f"\nOverall background process test result: {'PASSED' if overall_passed else 'FAILED'}")

if __name__ == "__main__":
    run_tests()