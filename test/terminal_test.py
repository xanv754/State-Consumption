import time
import unittest 
from utils.console import terminal


class TestTerminal(unittest.TestCase):
    """Test class to test the terminal."""

    def test_spinner(self):
        """Test the print method."""
        terminal.spinner(text="Test loading 1...")
        time.sleep(5)
        terminal.spinner(stop=True)
        terminal.spinner(text="Test loading 2...")
        time.sleep(5)
        terminal.spinner(stop=True)
        self.assertTrue(True)

    def test_print(self):
        """Test the print method."""
        terminal.print("[green3]Test print")


if __name__ == "__main__":
    unittest.main()