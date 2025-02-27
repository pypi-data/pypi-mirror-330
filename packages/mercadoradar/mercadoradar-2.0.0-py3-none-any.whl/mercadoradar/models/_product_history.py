import pprint
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel

class ProductHistory(BaseModel):
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: datetime
    product: Any
    sales_price: Optional[float] = None
    installment_price: Optional[float] = None
    regular_price: Optional[float] = None
    status: Any
    rating: Optional[float] = None
    reviews_quantity: Optional[int] = None
    reviews_one_star_quantity: Optional[int] = None
    reviews_two_star_quantity: Optional[int] = None
    reviews_three_star_quantity: Optional[int] = None
    reviews_four_star_quantity: Optional[int] = None
    reviews_five_star_quantity: Optional[int] = None
    sold_quantity: Optional[int] = None
    units_in_stock: Optional[int] = None

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