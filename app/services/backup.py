import shutil
from datetime import datetime
from pathlib import Path

from cryptography.fernet import Fernet

from app.config import BACKUP_ENCRYPTION_KEY

BACKUP_DIR = Path("backups")
DB_PATH = Path("database/erp.db")


def _get_fernet():
    if BACKUP_ENCRYPTION_KEY:
        return Fernet(BACKUP_ENCRYPTION_KEY.encode())
    return None


def _ensure_backup_dir():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def create_backup() -> dict:
    _ensure_backup_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    backup_name = f"erp_{timestamp}.db"
    backup_path = BACKUP_DIR / backup_name

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DB_PATH}")

    shutil.copy2(DB_PATH, backup_path)

    fernet = _get_fernet()
    if fernet:
        data = backup_path.read_bytes()
        encrypted = fernet.encrypt(data)
        backup_path.write_bytes(encrypted)

    return {
        "filename": backup_name,
        "timestamp": timestamp,
        "encrypted": fernet is not None
    }


def list_backups() -> list:
    _ensure_backup_dir()
    backups = []
    for f in sorted(BACKUP_DIR.glob("erp_*.db"), reverse=True):
        backups.append({
            "filename": f.name,
            "size": f.stat().st_size,
            "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
        })
    return backups


def restore_backup(filename: str) -> dict:
    backup_path = BACKUP_DIR / filename
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup not found: {filename}")

    if not DB_PATH.parent.exists():
        DB_PATH.parent.mkdir(parents=True)

    fernet = _get_fernet()
    if fernet:
        data = backup_path.read_bytes()
        decrypted = fernet.decrypt(data)
        DB_PATH.write_bytes(decrypted)
    else:
        shutil.copy2(backup_path, DB_PATH)

    return {
        "message": "Database restored successfully",
        "backup": filename
    }
