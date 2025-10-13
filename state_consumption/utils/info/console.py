import threading
import time
import rich
from rich.console import Console


class Terminal:
    """Class to print the data in the terminal."""
    _instance: "Terminal | None" = None
    _console: Console
    _lock: threading.Lock
    _spinner_thread: threading.Thread | None = None
    _spinner_running: bool = False
    _spinner_text: str | None = None

    def __new__(cls):
        if not hasattr(cls, '__instance'):
            cls._instance = super(Terminal, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self, '__initialized'):
            self._console = Console()
            self._lock = threading.Lock()
            self._initialized = True

    def _exec_spinner(self) -> None:
        """Execute the spinner in the terminal."""
        with self._lock:
            with rich.get_console().status(f"{self._spinner_text}\n", spinner="dots") as status:
                while self._spinner_running:
                    time.sleep(0.1)

    def print_spinner(self, text: str) -> None:
        """Print the text in the terminal."""
        if self._spinner_running: 
            self.spinner(stop=True)
        self._console.print(text)
        
    def print(self, text: str) -> None:
        rich.print(text)

    def spinner(self, text: str = "Loading...", stop: bool = False) -> None:
        """Start or stop a spinner in the terminal."""
        if self._spinner_thread: 
            self._spinner_running = False
            self._spinner_thread.join()
            self._spinner_thread = None
        if stop:
            if self._spinner_text:
                final_text = self._spinner_text.split(".")[0]
                self._spinner_text = None
                self._console.print(f"{final_text}... OK")
        else:
            self._spinner_text = text
            self._spinner_running = True
            self._spinner_thread = threading.Thread(target=self._exec_spinner)
            self._spinner_thread.start()


terminal = Terminal()