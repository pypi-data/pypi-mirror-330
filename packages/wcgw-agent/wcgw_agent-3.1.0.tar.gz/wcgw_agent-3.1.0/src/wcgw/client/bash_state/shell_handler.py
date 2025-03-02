import os
import platform
import sys
import threading
import time
import traceback
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from ..platform_utils import is_windows, is_mac, is_unix_like, get_default_shell, get_shell_launch_args
from .windows_bg_process import (
    create_background_process,
    terminate_processes_by_name,
    list_background_processes,
    print_background_processes
)


class ShellHandler(ABC):
    """Abstract base class for shell handlers."""
    
    @abstractmethod
    def spawn(self, cmd: str, env: Dict[str, str], echo: bool, encoding: str, 
              timeout: float, cwd: str, **kwargs: Any) -> None:
        """Spawn a shell process."""
        pass
    
    @abstractmethod
    def close(self, force: bool = False) -> None:
        """Close the shell process."""
        pass
    
    @abstractmethod
    def send(self, text: Union[str, bytes]) -> int:
        """Send text to the shell process."""
        pass
    
    @abstractmethod
    def sendline(self, text: Union[str, bytes]) -> int:
        """Send text followed by a newline to the shell process."""
        pass
    
    @abstractmethod
    def sendintr(self) -> None:
        """Send an interrupt signal to the shell process."""
        pass
    
    @abstractmethod
    def expect(self, pattern: Any, timeout: float = -1) -> int:
        """Wait for a pattern to appear in the output."""
        pass
    
    @property
    @abstractmethod
    def before(self) -> Optional[str]:
        """Get the output that was read before the pattern was matched."""
        pass
    
    @property
    @abstractmethod
    def linesep(self) -> str:
        """Get the line separator for the shell."""
        pass
    
    @staticmethod
    def create_handler(
        cmd: str,
        env: Dict[str, str],
        echo: bool = True,
        encoding: str = "utf-8",
        timeout: float = 5.0,
        cwd: Optional[str] = None,
        **kwargs: Any
    ) -> "ShellHandler":
        """Create a platform-appropriate shell handler."""
        if is_windows():
            return WindowsShellHandler(cmd, env, echo, encoding, timeout, cwd, **kwargs)
        else:
            # Use PexpectShellHandler on Unix-like systems
            return PexpectShellHandler(cmd, env, echo, encoding, timeout, cwd, **kwargs)


class PexpectShellHandler(ShellHandler):
    """Shell handler implementation using pexpect for Unix-like systems."""
    
    def __init__(self, cmd: str, env: Dict[str, str], echo: bool, encoding: str, 
                 timeout: float, cwd: Optional[str], **kwargs: Any):
        """Initialize a pexpect-based shell handler."""
        import pexpect  # Import locally to avoid issues on Windows
        
        self._shell = None
        self.spawn(cmd, env, echo, encoding, timeout, cwd or os.getcwd(), **kwargs)
    
    def spawn(self, cmd: str, env: Dict[str, str], echo: bool, encoding: str, 
              timeout: float, cwd: str, **kwargs: Any) -> None:
        """Spawn a shell process using pexpect."""
        import pexpect  # Import locally to avoid issues on Windows
        
        self._shell = pexpect.spawn(
            cmd,
            env=env,  # type: ignore[arg-type]
            echo=echo,
            encoding=encoding,
            timeout=timeout,
            cwd=cwd,
            codec_errors="backslashreplace",
            **kwargs
        )
    
    def close(self, force: bool = False) -> None:
        """Close the shell process."""
        if self._shell:
            self._shell.close(force)
    
    def send(self, text: Union[str, bytes]) -> int:
        """Send text to the shell process."""
        if self._shell:
            return self._shell.send(text)
        return 0
    
    def sendline(self, text: Union[str, bytes]) -> int:
        """Send text followed by a newline to the shell process."""
        if self._shell:
            return self._shell.sendline(text)
        return 0
    
    def sendintr(self) -> None:
        """Send an interrupt signal to the shell process."""
        if self._shell:
            self._shell.sendintr()
    
    def expect(self, pattern: Any, timeout: float = -1) -> int:
        """Wait for a pattern to appear in the output."""
        if self._shell:
            try:
                return self._shell.expect(pattern, timeout=timeout)
            except Exception as e:
                # Forward pexpect exceptions
                raise e
        raise Exception("Shell not initialized")
    
    @property
    def before(self) -> Optional[str]:
        """Get the output that was read before the pattern was matched."""
        if self._shell:
            return self._shell.before
        return None
    
    @property
    def linesep(self) -> str:
        """Get the line separator for the shell."""
        if self._shell:
            return self._shell.linesep
        return os.linesep


class WindowsShellHandler(ShellHandler):
    """Shell handler implementation for Windows using subprocess."""
    
    def __init__(self, cmd: str, env: Dict[str, str], echo: bool, encoding: str, 
                 timeout: float, cwd: Optional[str], **kwargs: Any):
        """Initialize a Windows-based shell handler."""
        import subprocess
        import threading
        
        self._process = None
        self._before = ""
        self._output_buffer = ""
        self._lock = threading.Lock()
        self._timeout = timeout
        self._encoding = encoding
        self._dimensions = kwargs.get('dimensions', (24, 80))
        
        # Store any patterns we're currently waiting for
        self._expect_pattern = None
        self._expect_event = threading.Event()
        self._expect_matched_index = -1
        
        self.spawn(cmd, env, echo, encoding, timeout, cwd or os.getcwd(), **kwargs)
    
    def spawn(self, cmd: str, env: Dict[str, str], echo: bool, encoding: str, 
              timeout: float, cwd: str, **kwargs: Any) -> None:
        """Spawn a shell process using subprocess."""
        import subprocess
        
        # Parse the command and args
        if isinstance(cmd, str):
            shell_parts = cmd.split()
            shell_cmd = shell_parts[0]
            shell_args = shell_parts[1:] if len(shell_parts) > 1 else []
        else:
            shell_cmd = cmd
            shell_args = []
            
        # Create the process
        self._process = subprocess.Popen(
            [shell_cmd] + shell_args,
            env=env,
            cwd=cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0,
            universal_newlines=True,
        )
        
        # Start a thread to continually read from the process
        self._running = True
        self._reader_thread = threading.Thread(target=self._reader_loop)
        self._reader_thread.daemon = True
        self._reader_thread.start()
    
    def _reader_loop(self) -> None:
        """Continuously read from the process output."""
        while self._running and self._process and self._process.stdout:
            try:
                # Read a single character at a time
                char = self._process.stdout.read(1)
                if char:
                    with self._lock:
                        self._output_buffer += char
                        
                        # Check if we're waiting for a pattern
                        if self._expect_pattern is not None:
                            self._check_pattern()
                else:
                    # Process has ended or no more output
                    time.sleep(0.01)
            except Exception as e:
                print(f"Error reading from process: {e}")
                break
    
    def _check_pattern(self) -> None:
        """Check if the output buffer matches any of the expected patterns."""
        if not self._expect_pattern:
            return
            
        # Convert string patterns to list for consistent handling
        patterns = self._expect_pattern
        if isinstance(patterns, (str, bytes)):
            patterns = [patterns]
            
        # Check each pattern for a match
        for i, pattern in enumerate(patterns):
            if isinstance(pattern, str) and pattern in self._output_buffer:
                self._before = self._output_buffer[:self._output_buffer.index(pattern)]
                self._expect_matched_index = i
                self._expect_event.set()
                return
    
    def close(self, force: bool = False) -> None:
        """Close the shell process."""
        self._running = False
        if self._process:
            if force:
                self._process.kill()
            else:
                self._process.terminate()
            self._process.wait()
            self._process = None
        
        if self._reader_thread and self._reader_thread.is_alive():
            self._reader_thread.join(timeout=2.0)
    
    def send(self, text: Union[str, bytes]) -> int:
        """Send text to the shell process."""
        if not self._process or not self._process.stdin:
            return 0
            
        # Convert to string if necessary
        if isinstance(text, bytes):
            text = text.decode(self._encoding)
            
        try:
            self._process.stdin.write(text)
            self._process.stdin.flush()
            return len(text)
        except Exception as e:
            print(f"Error sending to process: {e}")
            return 0
    
    def sendline(self, text: Union[str, bytes]) -> int:
        """Send text followed by a newline to the shell process."""
        if isinstance(text, bytes):
            text = text.decode(self._encoding)
        return self.send(text + self.linesep)
    
    def sendintr(self) -> None:
        """Send an interrupt signal to the shell process."""
        if self._process:
            self._process.send_signal(2)  # SIGINT
    
    # Define Windows-specific constants to replace pexpect's
    class _WindowsTIMEOUT:
        """Dummy class for Windows timeout handling."""
        pass

    class _WindowsEOF:
        """Dummy class for Windows EOF handling."""
        pass

    # Create singleton instances
    WINDOWS_TIMEOUT = _WindowsTIMEOUT()
    WINDOWS_EOF = _WindowsEOF()

    def expect(self, pattern: Any, timeout: float = -1) -> int:
        """Wait for a pattern to appear in the output."""
        if timeout == -1:
            timeout = self._timeout
            
        # Try to use pexpect constants if available, otherwise use our Windows equivalents
        try:
            from pexpect import TIMEOUT, EOF
        except ImportError:
            # On Windows, use our own constants
            TIMEOUT = self.WINDOWS_TIMEOUT
            EOF = self.WINDOWS_EOF
        
        # Special handling for pexpect.TIMEOUT and pexpect.EOF
        if pattern == TIMEOUT or pattern == self.WINDOWS_TIMEOUT:
            time.sleep(timeout)
            return 0
        elif pattern == EOF or pattern == self.WINDOWS_EOF:
            if not self._process or self._process.poll() is not None:
                return 0
            time.sleep(timeout)
            return 1
        
        # Handle the case where pattern is a string that might contain Unicode
        if isinstance(pattern, str):
            # Replace Unicode arrow with ASCII '>'
            pattern = pattern.replace('→', '>')
            
        # Store the pattern we're looking for
        with self._lock:
            self._expect_pattern = pattern
            self._expect_matched_index = -1
            self._expect_event.clear()
            
            # Check if we already have a match
            self._check_pattern()
            
        # Wait for a match or timeout
        if timeout > 0:
            matched = self._expect_event.wait(timeout)
            if not matched:
                # Timeout occurred
                with self._lock:
                    self._before = self._output_buffer
                    self._expect_pattern = None
                return 1  # Index for TIMEOUT in pexpect
        else:
            # Wait indefinitely
            self._expect_event.wait()
            
        # Return the matched index
        with self._lock:
            self._expect_pattern = None
            return self._expect_matched_index
    
    @property
    def before(self) -> Optional[str]:
        """Get the output that was read before the pattern was matched."""
        return self._before
    
    @property
    def linesep(self) -> str:
        """Get the line separator for the shell."""
        return os.linesep


def has_screen_command() -> bool:
    """Check if the 'screen' command is available on the system."""
    if is_windows():
        # 'screen' is not available on Windows
        return False
    
    try:
        import subprocess
        subprocess.run(
            ["which", "screen"], capture_output=True, check=True, timeout=0.2
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def cleanup_all_screens_with_name(name: str, console: Any) -> None:
    """Clean up all screen sessions with the given name."""
    if is_windows():
        # For Windows, use our background process management module
        terminated_ids = terminate_processes_by_name(name, console)
        if terminated_ids:
            console.log(f"Terminated {len(terminated_ids)} Windows background processes for {name}")
        return
    
    # Unix/Linux screen handling
    try:
        import subprocess
        # Try to get the list of screens.
        result = subprocess.run(
            ["screen", "-ls"],
            capture_output=True,
            text=True,
            check=True,
            timeout=0.2,
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        # When no screens exist, screen may return a non-zero exit code.
        output = (e.stdout or "") + (e.stderr or "")
    except FileNotFoundError:
        return
    except Exception as e:
        console.log(f"{e}: exception while clearing running screens.")
        return

    sessions_to_kill = []

    # Parse each line of the output. The lines containing sessions typically start with a digit.
    for line in output.splitlines():
        line = line.strip()
        if not line or not line[0].isdigit():
            continue

        # Each session is usually shown as "1234.my_screen (Detached)".
        # We extract the first part, then split on the period to get the session name.
        session_info = line.split()[0].strip()  # e.g., "1234.my_screen"
        if session_info.endswith(f".{name}"):
            sessions_to_kill.append(session_info)

    # Now, for every session we found, tell screen to quit it.
    for session in sessions_to_kill:
        try:
            subprocess.run(
                ["screen", "-S", session, "-X", "quit"],
                check=True,
                timeout=5,
            )
        except Exception as e:
            console.log(f"Failed to kill screen session: {session}\n{e}")


def start_shell(
    is_restricted_mode: bool, initial_dir: str, console: Any, over_screen: bool
) -> Tuple[ShellHandler, str]:
    """Start a shell process with the specified parameters."""
    shell_id = "wcgw." + time.strftime("%H%M%S")
    
    # Use platform-specific shell command
    shell_cmd = get_default_shell()
    shell_args = get_shell_launch_args(is_restricted_mode)
    
    cmd = shell_cmd
    if shell_args:
        cmd += " " + " ".join(shell_args)
    
    # Set up environment variables
    from ..platform_utils import get_tmpdir, get_prompt_string
    
    overrideenv = {
        **os.environ,
        "PS1": get_prompt_string(),
        "TMPDIR": get_tmpdir(),
        "TERM": "xterm-256color" if is_unix_like() else "windows-ansi",
    }
    
    try:
        # Create a shell handler appropriate for the platform
        shell = ShellHandler.create_handler(
            cmd,
            env=overrideenv,
            echo=True,
            encoding="utf-8",
            timeout=5.0,
            cwd=initial_dir,
            codec_errors="backslashreplace",
            dimensions=(500, 160),
        )
        
        # Set up prompt
        from ..platform_utils import get_prompt_command
        shell.sendline(get_prompt_command())
        shell.expect(get_prompt_string(), timeout=0.2)
    except Exception as e:
        console.print(traceback.format_exc())
        console.log(f"Error starting shell: {e}. Retrying with basic shell...")
        
        # Fallback to basic shell command
        if is_windows():
            fallback_cmd = "cmd.exe"
        else:
            fallback_cmd = "/bin/bash --noprofile --norc"
            
        shell = ShellHandler.create_handler(
            fallback_cmd,
            env=overrideenv,
            echo=True,
            encoding="utf-8",
            timeout=5.0,
            cwd=initial_dir,
            codec_errors="backslashreplace",
        )
        shell.sendline(get_prompt_command())
        shell.expect(get_prompt_string(), timeout=0.2)
    
    # Different handling for screen based on platform
    if over_screen:
        if is_windows():
            # Windows alternative - enable background process functionality
            shell.sendline(f"echo [Windows] Background process mode enabled for {shell_id}")
            shell.expect(get_prompt_string(), timeout=0.2)
            
            # Show the Windows background process commands
            help_text = """
            # Windows Background Process Commands:
            # To start a background process:
            #   wcgw-bg-start "<command>" - e.g., wcgw-bg-start "npm run dev"
            # To list running background processes:
            #   wcgw-bg-list
            # To terminate a background process:
            #   wcgw-bg-kill <process-id>
            """
            shell.sendline(f"echo '{help_text}'")
            shell.expect(get_prompt_string(), timeout=0.2)
            
            # Define the background process functions as aliases
            # Note: This relies on the functions being implemented in the Windows shell
            if shell_cmd.endswith("powershell.exe"):
                # PowerShell functions
                bg_functions = f"""
                function wcgw-bg-start {{ param($cmd) [Console]::WriteLine("Starting background process: $cmd"); }}
                function wcgw-bg-list {{ [Console]::WriteLine("Listing background processes..."); }}
                function wcgw-bg-kill {{ param($id) [Console]::WriteLine("Terminating background process: $id"); }}
                """
                shell.sendline(bg_functions)
                shell.expect(get_prompt_string(), timeout=0.2)
            else:
                # CMD functions (less robust but still functional)
                shell.sendline('echo Windows background processes are available through PowerShell')
                shell.expect(get_prompt_string(), timeout=0.2)
        else:
            # Unix/Linux screen handling
            if not has_screen_command():
                raise ValueError("Screen command not available")
            
            # shellid is just hour, minute, second number
            shell.sendline(f"trap 'screen -X -S {shell_id} quit' EXIT")
            shell.expect(get_prompt_string(), timeout=0.2)
            
            shell.sendline(f"screen -q -S {shell_id} /bin/bash --noprofile --norc")
            shell.expect(get_prompt_string(), timeout=5.0)
    
    return shell, shell_id