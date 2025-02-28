from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


class AttributeValue(BaseModel):
    created_at: datetime
    updated_at: datetime
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None
    id: int
    value: str
    attribute_type: Any
    display_order: int

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
