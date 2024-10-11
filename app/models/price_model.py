from pydantic import BaseModel
from app.models.currency_enum import CurrencyEnum


class PriceModel(BaseModel):
    amount: float
    currency_id: CurrencyEnum = CurrencyEnum.ARS