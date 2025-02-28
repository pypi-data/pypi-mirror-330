import pprint
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel

class Site(BaseModel):
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: datetime
    id: int
    name: str
    domain: Optional[str] = None
    currency: Optional[Any] = None
    currency_symbol: Optional[str] = None
    status: Optional[Any] = None
    is_marketplace: bool
    country: Optional[Any] = None
    language: Optional[Any] = None
    logo_url: Optional[str] = None
    thousand_separator: Any
    decimal_separator: Any

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