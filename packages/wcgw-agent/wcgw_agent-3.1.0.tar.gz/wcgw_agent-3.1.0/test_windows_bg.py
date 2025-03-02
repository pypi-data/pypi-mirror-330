"""
Test script for Windows background process management
"""
import os
import sys
import time

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath('src'))

from wcgw.client.platform_utils import is_windows
from wcgw.client.bash_state.windows_bg_process import (
    create_background_process,
    list_background_processes,
    print_background_processes,
    terminate_background_process
)

class MockConsole:
    """Simple console implementation for testing."""
    def __init__(self):
        self.logs = []
    
    def log(self, msg):
        self.logs.append(msg)
        print(f"[LOG] {msg}")
    
    def print(self, msg):
        print(f"[PRINT] {msg}")

def test_bg_processes():
    """Test Windows background process management"""
    
    if not is_windows():
        print("This test is specifically for Windows systems.")
        return
    
    console = MockConsole()
    
    print("\n=== Testing Windows Background Process Management ===")
    
    # Test 1: Create a long-running background process
    print("\n1. Creating a long-running background process...")
    proc_id1 = create_background_process(
        "echo Background process started && timeout /t 10 && echo Background process completed",
        "test-long-process",
        console
    )
    
    if not proc_id1:
        print("ERROR: Failed to create background process")
        return
    
    print(f"Created process with ID: {proc_id1}")
    
    # Test 2: Create a quick background process
    print("\n2. Creating a quick background process...")
    proc_id2 = create_background_process(
        "echo Quick process && timeout /t 2 && echo Quick process done",
        "test-quick-process",
        console
    )
    
    if not proc_id2:
        print("ERROR: Failed to create quick background process")
        return
    
    print(f"Created quick process with ID: {proc_id2}")
    
    # Test 3: List processes
    print("\n3. Listing background processes...")
    time.sleep(1)  # Give processes time to start
    processes = list_background_processes(console)
    
    for proc in processes:
        print(f"Process: {proc['id']}, Name: {proc['name']}, Status: {proc['status']}")
    
    # Test 4: Wait for quick process to complete
    print("\n4. Waiting for quick process to complete...")
    time.sleep(3)
    
    # List again to see status changes
    processes = list_background_processes(console)
    for proc in processes:
        print(f"Process: {proc['id']}, Name: {proc['name']}, Status: {proc['status']}")
    
    # Test 5: Terminate long process
    print("\n5. Terminating long-running process...")
    result = terminate_background_process(proc_id1, console)
    print(f"Termination result: {result}")
    
    # List again to confirm termination
    print("\n6. Final process list:")
    processes = list_background_processes(console)
    if not processes:
        print("No active processes - all terminated successfully")
    else:
        for proc in processes:
            print(f"Process: {proc['id']}, Name: {proc['name']}, Status: {proc['status']}")
    
    print("\n=== Windows Background Process Test Complete ===")

if __name__ == "__main__":
    test_bg_processes()