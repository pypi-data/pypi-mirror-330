import win32com.client
from .utils import is_autocad_running
from colorama import Fore, Style


class Cadvance:
    def __init__(self, debug=True):
        """Initialize the Cadvance object."""
        self.debug_v = debug
        self.autocad = None

        if is_autocad_running():
            self.autocad = win32com.client.Dispatch("AutoCAD.Application")

    def log(self, message, log_type="info"):
        """Log messages with the specified verbosity, color, and log type."""
        if self.debug_v:
            # Default log formatting and color
            log_prefix = "[ CadVance ]"
            if log_type == "info":
                color = Fore.CYAN
                log_level = "info"
            elif log_type == "warning":
                color = Fore.YELLOW
                log_level = "warning"
            elif log_type == "error":
                color = Fore.RED
                log_level = "Error"
            elif log_type == "success":
                color = Fore.GREEN
                log_level = "Success"
            else:
                color = Fore.WHITE
                log_level = "info"

            # Format and print the log message
            print(f"{color}{log_prefix} {log_level} : {message}{Style.RESET_ALL}")

    def is_cad_running(self):
        """Check if AutoCAD is running."""
        if is_autocad_running():
            self.log("AutoCAD is running.", "success")
            return True
        else:
            self.log("AutoCAD is not Running.", "error")
            return True

    def open_cad(self):
        """Open AutoCAD if it’s not already running."""
        if not is_autocad_running():
            try:
                self.autocad = win32com.client.Dispatch("AutoCAD.Application")
                self.autocad.Visible = True
                self.log("AutoCAD opened successfully.", "success")
                return True
            except Exception as e:
                self.log(f"Error connecting to AutoCAD: {e}", "error")
                return False
        else:
            if not self.autocad:
                self.autocad = win32com.client.Dispatch("AutoCAD.Application")
            self.log("AutoCAD is already running.", "warning")

    def cad_version(self):
        """Retrieve and log the installed AutoCAD version."""
        if self.autocad:
            try:
                version = self.autocad.Version
                self.log(f"Installed AutoCAD version: {version}", "info")
                return version
            except Exception as e:
                self.log(f"Error retrieving AutoCAD version: {e}", "error")
                return f"Error retrieving AutoCAD version: {e}"
        else:
            self.log("AutoCAD is not running. Cannot retrieve version.", "warning")
            return "AutoCAD is not running. Cannot retrieve version."

    def close_cad(self):
        """Close AutoCAD application."""
        if self.autocad:
            self.autocad.Quit()
            self.log("AutoCAD closed successfully.", "success")
        else:
            self.log("AutoCAD is not running.", "warning")
