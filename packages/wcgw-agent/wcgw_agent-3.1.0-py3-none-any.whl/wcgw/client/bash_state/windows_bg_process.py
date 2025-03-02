"""
Windows Background Process Management

This module provides a Windows alternative to Unix's 'screen' command.
It allows for creating, managing, and terminating background processes on Windows.
"""

import os
import subprocess
import threading
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

# Global registry of background processes
_windows_bg_processes = {}


def create_background_process(command: str, process_name: str, console: Any) -> str:
    """
    Create a Windows background process that simulates screen functionality.
    
    Args:
        command: The shell command to run in the background
        process_name: A name identifier for the process (similar to screen name)
        console: Logger interface for output
    
    Returns:
        process_id: Unique ID for the created process
    """
    global _windows_bg_processes
    
    # Generate a unique ID for this process
    process_id = str(uuid.uuid4())
    
    try:
        # Use a simpler approach for Windows background processes
        # Create a temporary batch file to run the command
        batch_file = os.path.join(os.environ.get('TEMP', '.'), f"{process_id}.bat")
        with open(batch_file, 'w') as f:
            f.write(f"@echo off\n{command}\n")
        
        # Use start command to run the batch file in the background
        start_command = f'start /b cmd /c "{batch_file}"'
        
        # Create the process
        process = subprocess.Popen(
            start_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Store in our registry
        _windows_bg_processes[process_id] = {
            "process": process,
            "name": process_name,
            "command": command,
            "created": time.time()
        }
        
        console.log(f"Started Windows background process: {process_id} for command: {command}")
        return process_id
        
    except Exception as e:
        console.log(f"Failed to create Windows background process: {e}")
        return None


def list_background_processes(console: Any) -> List[Dict[str, Any]]:
    """
    List all registered Windows background processes.
    
    Args:
        console: Logger interface for output
    
    Returns:
        List of process information dictionaries
    """
    global _windows_bg_processes
    result = []
    
    for process_id, process_info in list(_windows_bg_processes.items()):
        # Check if process is still running
        if process_info["process"].poll() is not None:
            status = f"Exited with code {process_info['process'].poll()}"
        else:
            status = "Running"
            
        result.append({
            "id": process_id,
            "name": process_info["name"],
            "command": process_info["command"],
            "status": status,
            "created": time.ctime(process_info["created"])
        })
    
    return result


def print_background_processes(console: Any) -> None:
    """
    Print all Windows background processes to the console.
    
    Args:
        console: Logger interface for output
    """
    processes = list_background_processes(console)
    
    if not processes:
        console.log("No Windows background processes running.")
        return
        
    console.log("Windows Background Processes:")
    for process in processes:
        console.log(f"ID: {process['id']}")
        console.log(f"  Name: {process['name']}")
        console.log(f"  Command: {process['command']}")
        console.log(f"  Status: {process['status']}")
        console.log(f"  Started: {process['created']}")
        console.log("---")


def terminate_background_process(process_id: str, console: Any) -> bool:
    """
    Terminate a specific Windows background process.
    
    Args:
        process_id: ID of the process to terminate
        console: Logger interface for output
        
    Returns:
        bool: True if termination was successful, False otherwise
    """
    global _windows_bg_processes
    
    if process_id not in _windows_bg_processes:
        console.log(f"Process ID {process_id} not found")
        return False
    
    process_info = _windows_bg_processes[process_id]
    
    try:
        # Terminate the subprocess
        if process_info["process"].poll() is None:
            process_info["process"].terminate()
            try:
                process_info["process"].wait(timeout=3)
            except subprocess.TimeoutExpired:
                process_info["process"].kill()
                
            console.log(f"Terminated Windows background process: {process_id}")
            
            # Remove from registry
            _windows_bg_processes.pop(process_id)
            return True
        else:
            console.log(f"Process {process_id} already terminated")
            _windows_bg_processes.pop(process_id)
            return True
    except Exception as e:
        console.log(f"Failed to terminate Windows background process {process_id}: {e}")
        return False


def terminate_processes_by_name(name: str, console: Any) -> List[str]:
    """
    Terminate all Windows background processes with the given name.
    
    Args:
        name: Name of the processes to terminate
        console: Logger interface for output
        
    Returns:
        List of terminated process IDs
    """
    global _windows_bg_processes
    terminated_ids = []
    
    for process_id, process_info in list(_windows_bg_processes.items()):
        if process_info["name"] == name:
            if terminate_background_process(process_id, console):
                terminated_ids.append(process_id)
                
    return terminated_ids