from typing import Optional

from ._api import MercadoRadarAPI
from ._models.product_attribute_value import ProductAttributeValue as ProductAttributeValueSchema
from .enums import AttributeValueType


class ProductAttributeValue:

    @classmethod
    def create(cls,
               product_id: int,
               attribute_type_id: int,
               attribute_value_id: Optional[int] = None,
               value: Optional[str] = None,
               value_type: Optional[AttributeValueType] = None,
               unit: Optional[str] = None,
               iso_value: Optional[str] = None,
               iso_value_type: Optional[AttributeValueType] = None,
               iso_unit: Optional[str] = None,
               is_verified: bool = False) -> ProductAttributeValueSchema:
        """
        Creates a new product attribute value association

        :param product_id: The ID of the product to which the attribute value is being assigned
        :param attribute_type_id: The ID of the attribute type
        :param attribute_value_id: The ID of a predefined attribute value (optional)
        :param value: A custom value for the attribute (optional)
        :param value_type: The type of the attribute value (e.g., TEXT, NUMERIC) (optional)
        :param unit: The unit of measurement for the attribute (optional)
        :param iso_value: The ISO-standardized value representation (optional)
        :param iso_value_type: The type of ISO value being provided (optional)
        :param iso_unit: The ISO unit of measurement (optional)
        :param is_verified: Indicates whether the attribute value is verified (default: False)

        :return: ProductAttributeValue instance with the created attribute data
        """

        api = MercadoRadarAPI()
        data = dict(
            product_id=product_id,
            attribute_type_id=attribute_type_id,
            attribute_value_id=attribute_value_id,
            value=value,
            value_type=value_type.value if value_type else None,
            unit=unit,
            iso_value=iso_value,
            iso_value_type=iso_value_type.value if iso_value_type else None,
            iso_unit=iso_unit,
            is_verified=is_verified
        )

        product_attribute_value = api.create_request(path='/v3/product-attribute-value/', data=data)

        return ProductAttributeValueSchema(**product_attribute_value)
