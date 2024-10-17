from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.di.dependencies import get_wallet_service
from app.dtos.wallet_dto import WalletDto
from app.models.transaction_model import TransactionModel
from app.models.wallet_model import WalletModel
from app.services.wallet_service import WalletService


router = APIRouter()


@router.post("", response_description="Agregar una nueva billetera", response_model=WalletDto)
async def create_wallet(wallet: WalletModel, wallet_service : WalletService = Depends(get_wallet_service)):
    wallet = await wallet_service.add_wallet(wallet.model_dump(by_alias=True, exclude_defaults=True, exclude_none=True))
    return wallet_service.get_wallet_dto(wallet)

@router.get("", response_description="Listar todas las billeteras", response_model=List[WalletModel])
async def get_wallets(wallet_service : WalletService = Depends(get_wallet_service)):
    wallets = await wallet_service.retrieve_wallets()
    return wallets

@router.get("/{id}", response_description="Obtener una billetera por ID", response_model=WalletDto)
async def get_wallet(id: str, wallet_service : WalletService = Depends(get_wallet_service)):
    wallet = await wallet_service.retrieve_wallet(id)
    if wallet:
        return wallet_service.get_wallet_dto(wallet)
    raise HTTPException(status_code=404, detail=f"Billetera con ID {id} no encontrada")


@router.put("/{id}", response_description="Actualizar una billetera", response_model=WalletDto)
async def update_wallet_data(id: str, wallet: WalletModel, wallet_service : WalletService = Depends(get_wallet_service)):
    wallet = {k: v for k, v in wallet.model_dump(by_alias=True, exclude_defaults=True, exclude_none=True).items() if v is not None}
    updated_wallet = await wallet_service.update_wallet(id, wallet)
    if updated_wallet:
        w = await wallet_service.retrieve_wallet(id)
        return wallet_service.get_wallet_dto(w)
    raise HTTPException(status_code=404, detail=f"Billetera con ID {id} no encontrada")


@router.delete("/{id}", response_description="Eliminar una billetera")
async def delete_wallet_data(id: str, wallet_service : WalletService = Depends(get_wallet_service)):
    deleted_wallet = await wallet_service.delete_wallet(id)
    if deleted_wallet:
        return "Billetera eliminada"
    raise HTTPException(status_code=404, detail=f"Billetera con ID {id} no encontrada")

@router.post("/{id}/transactions", response_description="Agregar una transacción a una billetera", response_model=WalletDto)
async def add_transaction_to_wallet(id: str,
                                    transaction: TransactionModel,
                                    wallet_service : WalletService = Depends(get_wallet_service)):
    wallet = await wallet_service.add_transaction_to_wallet(id, transaction.model_dump(by_alias=True, exclude_defaults=True, exclude_none=True))
    return wallet_service.get_wallet_dto(wallet)

