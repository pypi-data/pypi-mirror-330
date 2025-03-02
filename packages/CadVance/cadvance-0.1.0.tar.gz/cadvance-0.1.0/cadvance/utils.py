# cadvance/utils.py
import psutil

def is_autocad_running():
    """Check if AutoCAD is running by looking for its process in the system."""
    # List of possible AutoCAD process names
    autocad_processes = ['acad.exe', 'AutoCAD', 'acad']
    for process in psutil.process_iter(['name']):
        # Check if the process name matches any of the AutoCAD-related names
        if any(autocad_process.lower() in process.info['name'].lower() for autocad_process in autocad_processes):
            return True
    return False
