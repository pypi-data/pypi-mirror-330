import os
import sys
import platform

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "src/wcgw/client"))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Try to import platform_utils
try:
    from platform_utils import (
        is_windows,
        is_mac,
        is_unix_like,
        get_default_shell,
        get_shell_launch_args,
        get_prompt_string
    )
    
    # Print platform information
    print(f"Current platform: {platform.system()}")
    print(f"is_windows(): {is_windows()}")
    print(f"is_mac(): {is_mac()}")
    print(f"is_unix_like(): {is_unix_like()}")
    print(f"Default shell: {get_default_shell()}")
    print(f"Shell launch args: {get_shell_launch_args(False)}")
    print(f"Prompt string: {get_prompt_string()}")
    
    # For Windows, try to import Windows-specific modules
    if is_windows():
        try:
            from bash_state.windows_bg_process import (
                create_background_process,
                list_background_processes
            )
            print("Successfully imported Windows background process modules")
        except ImportError as e:
            print(f"Error importing Windows modules: {e}")
            
except ImportError as e:
    print(f"Error importing platform_utils: {e}")
    print(f"Python path: {sys.path}")