import pprint
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel

class Ticket(BaseModel):
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: datetime
    id: int
    title: str
    description: str
    responsible: Any
    customer: Optional[Any] = None
    status: Any
    days_open: int
    closed_at: datetime
    links: List[Any]
    opened_by_user: Any
    category: Any

    def to_str(self) -> str:
        data = self.model_dump()
        sorted_items = [('id', data.pop('id'))] if 'id' in data else []
        sorted_items += sorted(data.items())
        fields = "\n    ".join(f"{key}={value}" for key, value in sorted_items)

        return f"<{self.__class__.__name__}\n    {fields}\n>"

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.to_str()