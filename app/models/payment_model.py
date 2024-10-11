from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from app.models.currency_enum import CurrencyEnum
from app.models.price_model import PriceModel
from app.models import PyObjectId


class PaymentModel(PriceModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    payment_order_id: str
    connection_id: str
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "payment_order_id": "abc123",
                "connection_id": "fgh789",
                "amount": 1234.5,
                "currency_id": CurrencyEnum.ARS,
            }
        }