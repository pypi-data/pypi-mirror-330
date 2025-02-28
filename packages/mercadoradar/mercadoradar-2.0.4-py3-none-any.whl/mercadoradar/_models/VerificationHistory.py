from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class VerificationHistory(BaseModel):
    type: str
    object_type: str
    object_id: int
    is_verified: bool
    reason: Optional[str] = None
    suggestion: Optional[str] = None

    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: Optional[datetime] = None
