import threading
import time
import rich
from rich.console import Console


class Terminal:
    """Class to print the data in the terminal."""
    __instance: "Terminal | None" = None
    __console: Console
    __lock: threading.Lock
    __spinner_thread: threading.Thread | None = None
    __spinner_running: bool = False
    __spinner_text: str | None = None

    def __new__(cls):
        if not hasattr(cls, '__instance'):
            cls.__instance = super(Terminal, cls).__new__(cls)
            cls.__instance.__init__()
        return cls.__instance
    
    def __init__(self) -> None:
        if not hasattr(self, '__initialized'):
            self.__console = Console()
            self.__lock = threading.Lock()
            self.__initialized = True

    def __exec_spinner(self) -> None:
        """Execute the spinner in the terminal."""
        with self.__lock:
            with rich.get_console().status(f"{self.__spinner_text}\n", spinner="dots") as status:
                while self.__spinner_running:
                    time.sleep(0.1)

    def print(self, text: str) -> None:
        """Print the text in the terminal."""
        if self.__spinner_running: 
            self.spinner(stop=True)
        self.__console.print(text)

    def spinner(self, text: str = "Loading...", stop: bool = False) -> None:
        """Start or stop a spinner in the terminal."""
        if self.__spinner_thread: 
            self.__spinner_running = False
            self.__spinner_thread.join()
            self.__spinner_thread = None
        if stop:
            if self.__spinner_text:
                final_text = self.__spinner_text.split(".")[0]
                self.__spinner_text = None
                self.__console.print(f"{final_text}... OK")
        else:
            self.__spinner_text = text
            self.__spinner_running = True
            self.__spinner_thread = threading.Thread(target=self.__exec_spinner)
            self.__spinner_thread.start()
        


terminal = Terminal()