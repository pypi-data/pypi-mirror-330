from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


class ProductAttributeValue(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None
    id: Optional[int] = None
    product_id: Optional[int] = None
    attribute_value: Optional[Any] = None
    attribute_type: Optional[Any] = None
    value: Optional[str] = None
    value_type: Optional[Any] = None
    unit: Optional[str] = None
    iso_value: Optional[str] = None
    iso_value_type: Optional[Any] = None
    iso_unit: Optional[str] = None
    is_verified: Optional[bool] = None

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
