import pprint
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel

class Ticket(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    responsible: Optional[Any] = None
    customer: Optional[Any] = None
    status: Optional[Any] = None
    days_open: Optional[int] = None
    closed_at: Optional[datetime] = None
    links: Optional[List[Any]] = None
    opened_by_user: Optional[Any] = None
    category: Optional[Any] = None

    def to_str(self) -> str:
        data = self.model_dump()
        sorted_items = [('id', data.pop('id'))] if 'id' in data else []
        sorted_items += sorted(data.items())
        fields = "\n    ".join(f"{key}={value}" for key, value in sorted_items)

        return f"<{self.__class__.__name__}\n    {fields}\n>"

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        id = getattr(self, 'id', None)
        name = getattr(self, 'name', None)

        if id:
            return "<{self.__class__.name} id={self.id}>"
        elif id and name:
            return "<{self.__class__.name} id={self.id} name={self.name}>"
        else:
            return "<{self.__class__.name}>"
