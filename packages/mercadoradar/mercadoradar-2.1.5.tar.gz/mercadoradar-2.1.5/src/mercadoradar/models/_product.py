from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


class Product(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None
    id: Optional[int] = None
    name: Optional[str] = None
    sku_code: Optional[str] = None
    url: Optional[str] = None
    picture_url: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    site: Optional[Any] = None
    seller: Optional[Any] = None
    category: Optional[Any] = None
    category_verified_at: Optional[datetime] = None
    brand: Optional[Any] = None
    brand_verified_at: Optional[datetime] = None
    regular_price: Optional[float] = None
    sales_price: Optional[float] = None
    installment_price: Optional[float] = None
    previous_regular_price: Optional[float] = None
    previous_sales_price: Optional[float] = None
    previous_installment_price: Optional[float] = None
    price_updated_at: Optional[datetime] = None
    is_international_order: Optional[bool] = None
    is_kit: Optional[bool] = None
    is_kit_verified_at: Optional[datetime] = None
    is_kit_same_product: Optional[bool] = None
    is_kit_same_product_verified_at: Optional[datetime] = None
    units_per_kit: Optional[int] = None
    units_per_kit_verified_at: Optional[datetime] = None
    is_buy_box: Optional[bool] = None
    attributes: Optional[list] = None

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
