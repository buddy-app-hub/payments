from typing import Optional
from app.models.price_model import PriceModel
from app.models.wallet_model import WalletModel


class WalletDto(WalletModel):
    balance: Optional[PriceModel]
    total: Optional[PriceModel]