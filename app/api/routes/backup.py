from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.models.user import User
from app.services.permissions import require_admin
from app.services import backup as backup_service

router = APIRouter()


class RestoreRequest(BaseModel):
    filename: str


@router.post("/admin/backup")
def create_backup(admin: User = Depends(require_admin)):
    try:
        return backup_service.create_backup()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/admin/backups")
def list_backups(admin: User = Depends(require_admin)):
    return backup_service.list_backups()


@router.post("/admin/restore")
def restore_backup(
    request: RestoreRequest,
    admin: User = Depends(require_admin)
):
    try:
        return backup_service.restore_backup(request.filename)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
