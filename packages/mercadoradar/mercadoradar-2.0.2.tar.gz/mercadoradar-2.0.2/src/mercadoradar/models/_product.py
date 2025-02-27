import pprint
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel

class Product(BaseModel):
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: datetime
    id: int
    name: str
    sku_code: str
    url: str
    picture_url: str
    description: str
    status: str
    site: Any
    seller: Any
    category: Any
    category_verified_at: datetime
    brand: Any
    brand_verified_at: datetime
    regular_price: float
    sales_price: float
    installment_price: float
    previous_regular_price: float
    previous_sales_price: float
    previous_installment_price: float
    price_updated_at: datetime
    is_international_order: bool
    is_kit: bool
    is_kit_verified_at: datetime
    is_kit_same_product: bool
    is_kit_same_product_verified_at: datetime
    units_per_kit: int
    units_per_kit_verified_at: datetime
    is_buy_box: bool
    attributes: str

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