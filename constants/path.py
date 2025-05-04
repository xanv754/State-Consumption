from datetime import datetime

class PathStderr:
    MISSING_NODES_BOSS: str = f"/tmp/boss_missing_nodes_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    MISSING_NODES_ASF: str = f"/tmp/asf_missing_nodes_{datetime.now().strftime('%Y-%m-%d')}.xlsx"