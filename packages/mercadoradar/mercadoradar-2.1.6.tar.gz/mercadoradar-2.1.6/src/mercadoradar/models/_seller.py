import pprint
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel

class Seller(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None
    site: Optional[Any] = None
    corporate_identification_name: Optional[str] = None
    corporate_identification_type: Optional[str] = None
    corporate_identification_number: Optional[str] = None
    is_official_store: Optional[bool] = None
    type: Optional[Any] = None
    address: Optional[str] = None
    address_updated_at: Optional[datetime] = None
    street: Optional[str] = None
    street_number: Optional[str] = None
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    zip_code: Optional[str] = None
    city_name: Optional[str] = None
    state: Optional[str] = None
    uf: Optional[str] = None
    country: Optional[str] = None

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
