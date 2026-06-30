from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def log_action(
    db: Session,
    user_id: int,
    action: str,
    table_name: str,
    record_id: int = None,
    ip_address: str = None
):
    log = AuditLog(
        user_id=user_id,
        action=action,
        table_name=table_name,
        record_id=record_id,
        ip_address=ip_address
    )
    db.add(log)
    db.commit()
