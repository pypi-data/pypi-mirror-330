from colorama import  init
from datetime import datetime
import sys

init()

class Logger:
    def __init__(self, prefix: str = None, indent: int = 0):
        self.WHITE: str = "\u001b[37m"
        self.MAGENTA: str = "\x1b[38;2;157;38;255m"
        self.RED: str = "\x1b[38;5;196m"
        self.GREEN: str = "\x1b[38;5;40m"
        self.YELLOW: str = "\x1b[38;5;220m"
        self.BLUE: str = "\x1b[38;5;21m"
        self.LIGHTBLUE: str = "\x1b[94m"
        self.PINK: str = "\x1b[38;5;176m"
        self.GRAY: str = "\x1b[90m"
        self.CYAN: str = "\x1b[96m"
        self.prefix: str = f"{self.GRAY}[{self.MAGENTA}{prefix}{self.GRAY}] {self.WHITE}| " if prefix else ""
        self.indent: str = " " * indent
        self.debug_mode: bool = any(arg.lower() in ['--debug', '-debug'] for arg in sys.argv)

    @staticmethod
    def get_time() -> str:
        return datetime.now().strftime("%H:%M:%S")

    def get_taken(self, start: float = None, end: float = None) -> str:
        if start is not None and end is not None:
            if start > 1e12: start, end = start/1000, end/1000
            duration = end - start
            return f"{int(duration * 1000000)}µs" if duration < 0.001 else \
                f"{int(duration * 1000)}ms" if duration < 1 else \
                f"{str(duration)[:4]}s"
        return ""

    def message(self, level: str, message: str, start: int = None, end: int = None) -> str:
        time_now = f"{self.GRAY}[{self.MAGENTA}{self.get_time()}{self.GRAY}] {self.WHITE}|"
        taken = self.get_taken(start, end)
        timer = f" {self.MAGENTA}In{self.WHITE} -> {self.MAGENTA}{taken}" if taken else ""
        return f"{self.indent}{self.prefix}{time_now} {self.GRAY}[{level}{self.GRAY}] {self.WHITE}-> {self.GRAY}[{message}{self.GRAY}]{timer}"

    def success(self, message: str, level: str = "SCC", start: int = None, end: int = None) -> None:
        print(self.message(f"{self.GREEN}{level}", f"{self.GREEN}{message}", start, end))

    def warning(self, message: str, level: str = "WRN", start: int = None, end: int = None) -> None:
        print(self.message(f"{self.YELLOW}{level}", f"{self.YELLOW}{message}", start, end))

    def info(self, message: str, level: str = "INF", start: int = None, end: int = None) -> None:
        print(self.message(f"{self.LIGHTBLUE}{level}", f"{self.LIGHTBLUE}{message}", start, end))

    def failure(self, message: str, level: str = "ERR", start: int = None, end: int = None) -> None:
        print(self.message(f"{self.RED}{level}", f"{self.RED}{message}", start, end))

    def debug(self, message: str, level: str = "DBG", start: int = None, end: int = None) -> None:
        if self.debug_mode:
            print(self.message(f"{self.MAGENTA}{level}", f"{self.MAGENTA}{message}", start, end))

    def captcha(self, message: str, level: str = "CAP", start: int = None, end: int = None) -> None:
        print(self.message(f"{self.CYAN}{level}", f"{self.CYAN}{message}", start, end))

    def PETC(self):
        input(f"{self.indent}{self.GRAY}[{self.MAGENTA}Press Enter To Continue{self.GRAY}]")

    def __getattr__(self, name):
        if name.upper() in self.__dict__:
            def color(message: str, level: str = name.capitalize(), start: int = None, end: int = None):
                color_code = getattr(self, name.upper())
                print(self.message(f"{color_code}{level}", f"{color_code}{message}", start, end))
            return color
        raise AttributeError(f"'{self.__class__.__name__}' object has no attr '{name}'")