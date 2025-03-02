import os
import sys
import platform
import subprocess

def run_test():
    print("=== Basic Platform Detection Test ===")
    print(f"Platform system: {platform.system()}")
    print(f"Platform release: {platform.release()}")
    print(f"Platform version: {platform.version()}")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    print("\n=== Windows Process Test ===")
    if platform.system() == "Windows":
        print("Running on Windows, testing process management")
        try:
            # Test creating a background process on Windows
            test_file = os.path.join(os.getcwd(), "bg_test_output.txt")
            command = f'echo "Background process test" > {test_file}'
            
            # Use subprocess to run the command
            subprocess.Popen(command, shell=True)
            
            # Wait a bit
            import time
            time.sleep(2)
            
            # Check if the file was created
            if os.path.exists(test_file):
                with open(test_file, "r") as f:
                    content = f.read().strip()
                print(f"File created successfully with content: {content}")
                
                # Clean up
                os.unlink(test_file)
                print("Test file removed")
            else:
                print("File was not created")
        except Exception as e:
            print(f"Error in Windows process test: {e}")
    else:
        print("Not running on Windows, skipping Windows-specific tests")
    
    print("\n=== File System Test ===")
    try:
        # Test file creation and reading
        test_file = os.path.join(os.getcwd(), "test_file.txt")
        content = "This is a test file content"
        
        # Write to file
        with open(test_file, "w") as f:
            f.write(content)
        print(f"Created file: {test_file}")
        
        # Read from file
        with open(test_file, "r") as f:
            read_content = f.read()
        print(f"Read content: {read_content}")
        
        # Verify
        if read_content == content:
            print("File read/write test: PASSED")
        else:
            print("File read/write test: FAILED")
            
        # Clean up
        os.unlink(test_file)
        print("Test file removed")
    except Exception as e:
        print(f"Error in file system test: {e}")
    
    print("\n=== Command Execution Test ===")
    try:
        # Test command execution
        if platform.system() == "Windows":
            command = "echo Hello, Windows!"
        else:
            command = "echo Hello, Unix!"
            
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"Command output: {result.stdout}")
        
        if "Hello" in result.stdout:
            print("Command execution test: PASSED")
        else:
            print("Command execution test: FAILED")
    except Exception as e:
        print(f"Error in command execution test: {e}")

if __name__ == "__main__":
    run_test()