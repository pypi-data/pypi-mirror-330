import os
import platform
import sys

print("=== Simple Windows Compatibility Test ===")
print(f"Current Python version: {sys.version}")
print(f"Current platform: {platform.system()} {platform.release()}")
print(f"Current directory: {os.getcwd()}")

# Try importing from our module structure
try:
    sys.path.insert(0, os.path.abspath('src'))
    from wcgw.client.platform_utils import is_windows, is_mac, is_unix_like
    print(f"Successfully imported platform utils:")
    print(f"  is_windows(): {is_windows()}")
    print(f"  is_mac(): {is_mac()}")
    print(f"  is_unix_like(): {is_unix_like()}")
except ImportError as e:
    print(f"Error importing: {e}")
    # Define fallbacks
    print("Using fallback platform detection:")
    print(f"  is_windows(): {platform.system() == 'Windows'}")
    print(f"  is_mac(): {platform.system() == 'Darwin'}")
    print(f"  is_unix_like(): {os.name == 'posix'}")

# Try running a Windows command
try:
    import subprocess
    print("\nRunning 'dir' command:")
    result = subprocess.run("dir", shell=True, capture_output=True, text=True)
    print(f"Command exited with code: {result.returncode}")
    if result.stdout:
        print(f"First 3 lines of output:")
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines[:3]):
            print(f"  {line}")
except Exception as e:
    print(f"Error running command: {e}")

print("\n=== Test Complete ===")