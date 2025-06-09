import unittest
import pandas as pd
from utils.format import FixFormat


class TestFormat(unittest.TestCase):
    """Test class to test the format of the data."""

    def test_fix_column_word(self):
        """Test the fix of the format of a column."""
        df = pd.DataFrame({"COLUMN": ["ß", "┴", "Ú", "Ý", "=", "¾", "·", "±", "&#209"]})
        df_fixed = FixFormat.column_word(df, "COLUMN")
        self.assertTrue(df_fixed["COLUMN"][0] == "A")
        self.assertTrue(df_fixed["COLUMN"][1] == "A")
        self.assertTrue(df_fixed["COLUMN"][2] == "E")
        self.assertTrue(df_fixed["COLUMN"][3] == "I")
        self.assertTrue(df_fixed["COLUMN"][4] == "O")
        self.assertTrue(df_fixed["COLUMN"][5] == "O")
        self.assertTrue(df_fixed["COLUMN"][6] == "U")
        self.assertTrue(df_fixed["COLUMN"][7] == "Ñ")
        self.assertTrue(df_fixed["COLUMN"][8] == "Ñ")

    def test_fix_word(self):
        """Test the fix of the format of a word."""
        word = "ÁÉÍÓÚ-_áéíóú"
        word_fixed = FixFormat.word(word)
        self.assertTrue(word_fixed == "AEIOU  AEIOU")

    def test_fix_ip(self):
        """Test the fix of the format of an IP."""
        ip_string_case_one = "10.25.255.25"
        ip_string_case_two = "10..119...1..157"
        ip_number_case_one = 10255255255
        ip_number_case_two = 1025525255
        ip_string_fixed_case_one = FixFormat.ip(ip_string_case_one)
        ip_string_fixed_case_two = FixFormat.ip(ip_string_case_two)
        ip_number_fixed_case_one = FixFormat.ip(ip_number_case_one)
        ip_number_fixed_case_two = FixFormat.ip(ip_number_case_two)

        self.assertTrue(ip_string_fixed_case_one == ip_string_case_one)
        self.assertTrue(ip_string_fixed_case_two == "10.119.1.157")
        self.assertTrue(ip_number_fixed_case_one == "10.255.255.255")
        self.assertTrue(ip_number_fixed_case_two == "1.025.525.255")


if __name__ == "__main__":
    unittest.main()