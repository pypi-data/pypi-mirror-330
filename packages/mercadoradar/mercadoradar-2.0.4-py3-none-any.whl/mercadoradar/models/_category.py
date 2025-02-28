import pprint
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel

class Category(BaseModel):
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: datetime
    id: str
    name: str
    path_from_root: Optional[Any] = None
    children_categories: Optional[Any] = None
    domain_id: Optional[str] = None
    parent: Optional[str] = None
    path: str

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