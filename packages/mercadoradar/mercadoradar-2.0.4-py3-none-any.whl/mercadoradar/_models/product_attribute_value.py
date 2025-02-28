from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.mercadoradar.enums import AttributeValueType


class ProductAttributeValue(BaseModel):
    id: int = Field(..., description="Unique identifier")
    product_id: int = Field(..., description="ID of the associated product")

    attribute_value_id: Optional[int] = Field(None, description="ID of the attribute value")
    attribute_value: Optional[dict] = Field(None, description="Nested attribute value")

    attribute_type_id: Optional[int] = Field(None, description="ID of the attribute type")
    attribute_type: Optional[dict] = Field(None, description="Nested attribute type")

    value: Optional[str] = Field(None, description="The actual value of the attribute")
    value_type: Optional[AttributeValueType] = Field(None, description="Type of the value")

    unit: Optional[str] = Field(None, description="Unit of measurement")
    iso_value: Optional[str] = Field(None, description="ISO standardized value")
    iso_value_type: Optional[AttributeValueType] = Field(None, description="ISO value type")
    iso_unit: Optional[str] = Field(None, description="ISO unit of measurement")

    is_verified: bool = Field(False, description="Indicates if the attribute value is verified")

    created_at: datetime = Field(..., description="Timestamp when the record was created")
    updated_at: datetime = Field(..., description="Timestamp when the record was last updated")

    deleted_at: Optional[datetime] = Field(None, description="Timestamp when the record was deleted, if applicable")
    is_deleted: bool = Field(False, description="Indicates if the record is marked as deleted")
