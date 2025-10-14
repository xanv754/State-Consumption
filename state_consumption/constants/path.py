from os import path
from pathlib import Path
from datetime import datetime


ROOT_PATH = path.abspath(path.join(path.dirname(__file__), "..", ".."))
TMP_PATH = path.join(ROOT_PATH, "tmp")


class PathStderr:
    MISSING_NODES_BOSS: str = path.join(
        TMP_PATH, f"boss_missing_nodes_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    )
    MISSING_NODES_ASF: str = path.join(
        TMP_PATH, f"asf_missing_nodes_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    )
    MISSING_CONSUMPTION: str = path.join(
        TMP_PATH, f"missing_consumption_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    )

    def __init__(self):
        path = Path(TMP_PATH)
        path.mkdir(parents=True, exist_ok=True)
