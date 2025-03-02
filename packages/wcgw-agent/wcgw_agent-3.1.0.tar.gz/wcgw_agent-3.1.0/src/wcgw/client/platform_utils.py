import os
import platform
import subprocess
from typing import Optional, Tuple, List, Dict, Any


def is_windows() -> bool:
    """Check if the current platform is Windows."""
    return platform.system() == "Windows"


def is_mac() -> bool:
    """Check if the current platform is macOS."""
    return platform.system() == "Darwin"


def is_linux() -> bool:
    """Check if the current platform is Linux."""
    return platform.system() == "Linux"


def is_unix_like() -> bool:
    """Check if the current platform is Unix-like (macOS or Linux)."""
    return is_mac() or is_linux()


def get_default_shell() -> str:
    """Get the default shell command for the current platform."""
    if is_windows():
        # Use PowerShell as the default shell on Windows
        return "powershell.exe"
    else:
        # Use bash as the default shell on Unix-like systems
        return "/bin/bash"


def get_shell_launch_args(restricted_mode: bool = False) -> List[str]:
    """Get platform-specific shell launch arguments."""
    if is_windows():
        args = ["-NoProfile"]
        if restricted_mode:
            args.append("-ExecutionPolicy Restricted")
        return args
    else:
        args = []
        if restricted_mode:
            args.append("-r")
        return args


def get_tmpdir() -> str:
    """Get platform-appropriate temp directory."""
    if is_windows():
        return os.environ.get("TEMP", "")
    
    current_tmpdir = os.environ.get("TMPDIR", "")
    if current_tmpdir or not is_mac():
        return current_tmpdir
    try:
        # Fix issue while running ocrmypdf -> tesseract -> leptonica, set TMPDIR
        # https://github.com/tesseract-ocr/tesseract/issues/4333
        result = subprocess.check_output(
            ["getconf", "DARWIN_USER_TEMP_DIR"],
            text=True,
            timeout=5,
        ).strip()
        return result
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "//tmp"
    except Exception:
        return ""


def normalize_path(path: str) -> str:
    """Normalize path for the current platform."""
    return os.path.normpath(path)


def join_path(*parts: str) -> str:
    """Join path parts in a platform-appropriate way."""
    return os.path.join(*parts)


def get_prompt_string() -> str:
    """Get a prompt string that works across platforms."""
    return "wcgw> "


def get_prompt_command() -> str:
    """Get a command to set the prompt that works across platforms."""
    if is_windows():
        # PowerShell prompt
        return "function prompt { 'wcgw> ' }"
    else:
        # Bash prompt
        return "export GIT_PAGER=cat PAGER=cat PROMPT_COMMAND= PS1='wcgw>'' '"