from datetime import datetime
import sys

class Croustiistuff:
    def __init__(self, prefix: str = None, indent: int = 0, mode: str = "classic", separator: str = " "):
        self.colors = {
            'white': "\u001b[37m",
            'magenta': "\x1b[38;2;157;38;255m",
            'error': "\x1b[38;5;202m",
            'success': "\x1b[38;5;219m",
            'warning': "\x1b[38;5;214m",
            'blue': "\x1b[38;5;21m",
            'info': "\x1b[38;5;62m",
            'pink': "\x1b[38;5;176m",
            'gray': "\x1b[90m",
            'captcha': "\x1b[38;5;105m"
        }
        self.prefix: str = f"{self.colors['gray']}[{self.colors['magenta']}{prefix}{self.colors['gray']}] {self.colors['white']}→ " if prefix else ""
        self.indent: str = " " * indent
        self.debug_mode: bool = any(arg.lower() in ['--debug', '-debug'] for arg in sys.argv)
        self.mode = mode  # Modes: "classic" or "minimal"
        self.separator = separator  # Custom separator for minimal mode

    def get_time(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def _log(self, color: str, message: str, level: str) -> None:
        time_now = f"{self.colors['gray']}{self.get_time()}"
        
        if self.mode == "classic":
            formatted_msg = f"{self.indent}{self.prefix}{self.colors['gray']}[{time_now}] {self.colors['white']}→ {self.colors['gray']}[{color}{level}{self.colors['gray']}] {self.colors['white']}→ {self.colors['gray']}[{color}{message}{self.colors['gray']}]"
        elif self.mode == "minimal":
            formatted_msg = f"{self.colors['gray']}{time_now} {color}{level} {self.colors['white']}{self.separator} {self.colors['white']}{message}"
        
        print(formatted_msg)

    def success(self, message: str, level: str = "SUCCESS") -> None:
        self._log(self.colors['success'], message, level)

    def warning(self, message: str, level: str = "WARNING") -> None:
        self._log(self.colors['warning'], message, level)

    def info(self, message: str, level: str = "INFO") -> None:
        self._log(self.colors['info'], message, level)

    def error(self, message: str, level: str = "ERROR") -> None:
        self._log(self.colors['error'], message, level)

    def debug(self, message: str, level: str = "DEBUG") -> None:
        if self.debug_mode: 
            self._log(self.colors['magenta'], message, level)

    def captcha(self, message: str, level: str = "CAPTCHA") -> None:
        self._log(self.colors['captcha'], message, level)
