from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from app.models import PyObjectId
from app.models.transaction_model import TransactionModel


class WalletModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    transactions: list[TransactionModel]
    
    class Config:
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "transactions": [],
            }
        }
        