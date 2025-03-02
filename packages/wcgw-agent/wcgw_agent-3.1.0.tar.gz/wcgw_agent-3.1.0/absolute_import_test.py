import os
import sys
import time
import platform

# Add the module paths
sys.path.insert(0, os.path.abspath('.'))

# Simple console class
class TestConsole:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.logs = []
    
    def log(self, message):
        self.logs.append(message)
        if self.verbose:
            print(f"[LOG] {message}")
    
    def print(self, message, *args, **kwargs):
        self.log(message)

# Test function
def main():
    print(f"Current system: {platform.system()}")
    
    if platform.system() != "Windows":
        print("Not on Windows, skipping tests")
        return
    
    print("Running on Windows, testing background process functionality")
    
    # Import the necessary modules
    try:
        from src.wcgw.client.platform_utils import is_windows
        print(f"is_windows(): {is_windows()}")
        
        # Import the Windows background process module
        from src.wcgw.client.bash_state.windows_bg_process import (
            create_background_process,
            list_background_processes,
            print_background_processes,
            terminate_background_process
        )
        
        console = TestConsole()
        
        # Test creating a background process
        test_file = os.path.join(os.getcwd(), "bg_process_test.txt")
        if os.path.exists(test_file):
            os.unlink(test_file)
        
        print("\nCreating background process...")
        command = f'echo "Background process test" > "{test_file}" & timeout /t 5'
        process_id = create_background_process(command, "test_process", console)
        print(f"Process ID: {process_id}")
        
        # Wait for file to be created
        time.sleep(2)
        
        # Check if file was created
        if os.path.exists(test_file):
            with open(test_file, "r") as f:
                content = f.read().strip()
            print(f"File content: {content}")
            file_test_passed = "Background process test" in content
            print(f"File creation test: {'PASSED' if file_test_passed else 'FAILED'}")
        else:
            print("File was not created")
            file_test_passed = False
        
        # List processes
        print("\nListing processes...")
        processes = list_background_processes(console)
        print(f"Number of processes: {len(processes)}")
        process_found = any(p["id"] == process_id for p in processes)
        print(f"Process listing test: {'PASSED' if process_found else 'FAILED'}")
        
        # Terminate process
        print("\nTerminating process...")
        result = terminate_background_process(process_id, console)
        print(f"Termination result: {result}")
        
        # List processes again
        print("\nListing processes after termination...")
        processes_after = list_background_processes(console)
        print(f"Number of processes: {len(processes_after)}")
        process_exists_after = any(p["id"] == process_id for p in processes_after)
        print(f"Process termination test: {'PASSED' if not process_exists_after else 'FAILED'}")
        
        # Clean up
        if os.path.exists(test_file):
            os.unlink(test_file)
            print("Test file removed")
        
        # Overall test result
        overall_passed = file_test_passed and process_found and result and not process_exists_after
        print(f"\nOverall test result: {'PASSED' if overall_passed else 'FAILED'}")
        
    except ImportError as e:
        print(f"Import error: {e}")
        # Print the Python path
        print("\nPython path:")
        for p in sys.path:
            print(f"  {p}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()