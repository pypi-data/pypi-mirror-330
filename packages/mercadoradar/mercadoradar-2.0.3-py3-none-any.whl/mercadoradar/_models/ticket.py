from datetime import datetime, Optional
from typing import List

from pydantic import BaseModel, Field

from src.mercadoradar.enums import TicketStatus, TicketCategory


class Ticket(BaseModel):
    id: int = Field(..., description="Unique identifier")
    responsible: Optional[dict] = Field(None, description="Nested responsible user details")

    title: str = Field(..., description="Title of the ticket")
    description: str = Field(..., description="Detailed description of the issue")

    customer: dict = Field(..., description="Nested customer details")

    closed_at: Optional[datetime] = Field(None, description="Timestamp when the ticket was closed")
    status: TicketStatus = Field(TicketStatus.PENDING, description="Current status of the ticket")

    links: Optional[List[str]] = Field(None, description="List of related links")

    opened_by_user: Optional[dict] = Field(None, description="Nested opened-by user details")

    category: TicketCategory = Field(..., description="Category of the ticket")

    days_open: int = Field(..., description="Number of days the ticket has been open")

    created_at: datetime = Field(..., description="Timestamp when the record was created")
    updated_at: datetime = Field(..., description="Timestamp when the record was last updated")

    deleted_at: Optional[datetime] = Field(None, description="Timestamp when the record was deleted, if applicable")
    is_deleted: bool = Field(False, description="Indicates if the record is marked as deleted")
