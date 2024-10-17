from app.models.created_at_model import CreatedUpdatedAt
from app.models.price_model import PriceModel
from app.models.transaction_status_enum import TransactionStatus
from app.models.transaction_type import TransactionType


class TransactionModel(PriceModel, CreatedUpdatedAt):
    payment_id: str
    type: TransactionType
    status: TransactionStatus
    description: str
    
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "payment_id": "abc123",
                "type": TransactionType.deposit,
                "status": TransactionStatus.approved,
                "amount": 1234.5,
                "currency": "ARS",
                "description": "Ernestina",
            }
        }