from functools import lru_cache
from fastapi import Depends
from mercadopago import SDK
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from app.config.config import Settings
from app.services.payment_service import PaymentService
from app.services.wallet_service import WalletService


@lru_cache
def get_settings() -> Settings:
    return Settings()

def _get_sdk(settings: Settings = Depends(get_settings)) -> SDK:
    return SDK(settings.mercadopago_token)

def _get_mongo_connection(settings: Settings = Depends(get_settings)) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(settings.mongo_db)

def _get_buddy_db(connection = Depends(_get_mongo_connection)) -> AsyncIOMotorDatabase:
    return connection.buddy

def get_payments_collection(db = Depends(_get_buddy_db)) -> AsyncIOMotorCollection:
    return db.get_collection("payments")

def get_wallet_collection(db = Depends(_get_buddy_db)) -> AsyncIOMotorCollection:
    return db.get_collection("wallet")

def get_payment_service(sdk: SDK = Depends(_get_sdk), payments_collection : AsyncIOMotorCollection = Depends(get_payments_collection)) -> PaymentService:
    return PaymentService(mercado_pago=sdk, payments_collection=payments_collection)

def get_wallet_service(wallets_collection : AsyncIOMotorCollection = Depends(get_wallet_collection)) -> WalletService:
    return WalletService(wallet_collection=wallets_collection)
