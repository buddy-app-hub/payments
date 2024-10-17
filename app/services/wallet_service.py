from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

from app.dtos.wallet_dto import WalletDto
from app.models.payment_model import PaymentModel
from app.models.price_model import PriceModel
from app.models.transaction_model import TransactionModel
from app.models.transaction_status_enum import TransactionStatus
from app.models.transaction_type import TransactionType
from app.models.wallet_model import WalletModel


class WalletService:

    def __init__(self, wallet_collection : AsyncIOMotorCollection) -> None:
        self.wallet_collection = wallet_collection
    
    async def retrieve_wallets(self):
        wallets = []
        async for wallet in self.wallet_collection.find():
            wallets.append(WalletModel(**wallet))
        return wallets

    async def add_wallet(self, wallet_data: dict) -> WalletModel:
        wallet = await self.wallet_collection.insert_one(wallet_data)
        new_wallet = await self.wallet_collection.find_one({"_id": wallet.inserted_id})
        return WalletModel(**new_wallet)

    async def retrieve_wallet(self, id: str) -> WalletModel:
        wallet = await self.wallet_collection.find_one({"_id": ObjectId(id)})
        if wallet:
            return WalletModel(**wallet)

    async def update_wallet(self, id: str, data: dict):
        if len(data) < 1:
            return False
        wallet = await self.wallet_collection.find_one({"_id": ObjectId(id)})
        if wallet:
            updated_wallet = await self.wallet_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": data}
            )
            if updated_wallet:
                return True
        return False

    async def delete_wallet(self, id: str):
        wallet = await self.wallet_collection.find_one({"_id": ObjectId(id)})
        if wallet:
            await self.wallet_collection.delete_one({"_id": ObjectId(id)})
            return True
        
    async def add_transaction_to_wallet(self, id: str, transaction_data: dict):
        wallet = await self.retrieve_wallet(id)
        if wallet:
            wallet.transactions.append(TransactionModel(**transaction_data))
            updated_wallet = await self.wallet_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": wallet.dict(exclude="id")}
            )
            if updated_wallet:
                return await self.retrieve_wallet(id)
        return
    
    def get_transaction_from_payment(self, payment : PaymentModel, description: str):
        return TransactionModel(
            payment_id=payment.id,
            type=TransactionType.deposit,
            status=TransactionStatus.pending,
            amount=payment.amount * self.get_commision(),
            currency_id=payment.currency_id,
            description=description,
        )
        
    def get_commision(self):
        return 0.9
        
    def get_wallet_dto(self, wallet: WalletModel):
        balance = self.get_balance(wallet)
        total = self.get_total(wallet)
        return WalletDto(
            _id=ObjectId(wallet.id),
            transactions=wallet.transactions,
            balance=balance,
            total=total,
        )
        
    def get_balance(self, wallet: WalletModel):
        deposits = sum([tx.amount
                    if TransactionStatus.approved == tx.status and TransactionType.deposit == tx.type
                    else 0 
                    for tx in wallet.transactions
                    ])
        withdrawals = sum([tx.amount
                    if TransactionStatus.approved == tx.status and TransactionType.withdraw == tx.type
                    else 0 
                    for tx in wallet.transactions
                    ])
        balance = deposits - withdrawals
        if balance > 0:
            return PriceModel(amount=balance, currency=wallet.transactions[0].currency_id)
        return None
    
    def get_total(self, wallet: WalletModel):
        total = sum([tx.amount
                    if TransactionStatus.approved == tx.status and TransactionType.deposit == tx.type
                    else 0
                    for tx in wallet.transactions
                    ])
        
        if total > 0:
            return PriceModel(amount=total, currency=wallet.transactions[0].currency_id)
        return None