from datetime import datetime

class Filepath:
    MISSING_NODES: str = f"/tmp/missing_nodes_{datetime.now().strftime('%Y-%m-%d')}.xlsx"