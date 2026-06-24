import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def ensure_db():
    from modules.database import db_exists
    if not db_exists():
        from modules.collect_data import run
        run()

if __name__ == "__main__":
    ensure_db()