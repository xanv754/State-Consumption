import pandas as pd
from common.utils.fix import fix_column_word, fix_format_word, fix_ip

BAD_IP = 192168234123
GOOD_IP = "192.168.234.123"
DATA = {"WORD": ["ß┴ÚÝ=¾·±&#209"]}
SECOND_BAD_WORD = "-Á-É_Í-Ó_Ú_"

def test_fix_column_word():
    df = pd.DataFrame(DATA)
    df_fixed = fix_column_word(df, "WORD")
    assert df_fixed.equals(pd.DataFrame({"WORD": ["aAéíóóúñÑ"]}))

def test_fix_format_word():
    assert fix_format_word(SECOND_BAD_WORD) == "A E I O U"

def test_fix_ip():
    assert fix_ip(BAD_IP) == "192.168.234.123" and fix_ip(GOOD_IP) == GOOD_IP