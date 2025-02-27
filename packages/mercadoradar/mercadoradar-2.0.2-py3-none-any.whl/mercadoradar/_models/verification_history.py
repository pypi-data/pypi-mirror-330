from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class VerificationHistory(BaseModel):
    type: str = Field(..., description="The type of verification being performed (e.g., 'document', 'email').")
    object_type: str = Field(...,
                             description="The category of the object being verified (e.g., 'user', 'transaction').")
    object_id: int = Field(..., description="The unique identifier of the object being verified.")
    is_verified: bool = Field(..., description="Indicates whether the object has been verified.")

    reason: Optional[str] = Field(None, description="The reason why the verification failed, if applicable.")
    suggestion: Optional[str] = Field(None, description="Suggested actions to resolve the verification issue.")

    created_at: datetime = Field(..., description="Timestamp when the verification history record was created.")
    updated_at: datetime = Field(..., description="Timestamp when the verification history record was last updated.")

    is_deleted: bool = Field(False, description="Indicates whether this verification history record has been deleted.")
    deleted_at: Optional[datetime] = Field(None, description="Timestamp when the record was deleted, if applicable.")

    class Config:
        orm_mode = True
