import pprint
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel

class Seller(BaseModel):
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: datetime
    id: int
    name: str
    url: Optional[str] = None
    site: Any
    corporate_identification_name: Optional[str] = None
    corporate_identification_type: Optional[str] = None
    corporate_identification_number: Optional[str] = None
    is_official_store: Optional[bool] = None
    type: Optional[Any] = None
    address: Optional[str] = None
    address_updated_at: datetime
    street: str
    street_number: str
    complement: str
    neighborhood: str
    zip_code: str
    city_name: str
    state: str
    uf: str
    country: str

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