from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.di.dependencies import get_payment_service, get_wallet_service
from app.models.payment_model import PaymentModel
from app.models.payment_notification import PaymentNotification
from app.services.payment_service import PaymentService
from app.services.wallet_service import WalletService


router = APIRouter()


@router.get("/init")
def init_payment(connection_id: str, payment_service : PaymentService = Depends(get_payment_service)):
    return payment_service.handshake(connection_id)

@router.post("/webhook")
async def webhook(notification: PaymentNotification,
                  payment_service : PaymentService = Depends(get_payment_service),
                  ):
    if notification.data and "id" in notification.data:
        payment_id = notification.data["id"]
        
        payment = await payment_service.get_payment(payment_id)
        await payment_service.process_payment(payment)
    else:
        raise HTTPException(status_code=400, detail="Invalid notification")

@router.post("", response_description="Agregar un nuevo pago", response_model=PaymentModel)
async def create_payment(payment: PaymentModel,
                         description: str,
                         wallet_id: str,
                         payment_service : PaymentService = Depends(get_payment_service),
                         wallet_service : WalletService = Depends(get_wallet_service),
                         ):
    payment = await payment_service.add_payment(payment.model_dump(by_alias=True, exclude_defaults=True, exclude_none=True))
    transaction = wallet_service.get_transaction_from_payment(payment, description)
    await wallet_service.add_transaction_to_wallet(wallet_id, transaction.model_dump(by_alias=True, exclude_defaults=True, exclude_none=True))
    return payment

@router.get("", response_description="Listar todos los pagos", response_model=List[PaymentModel])
async def get_payments(payment_service : PaymentService = Depends(get_payment_service)):
    payments = await payment_service.retrieve_payments()
    return payments

@router.get("/{id}", response_description="Obtener un pago por ID", response_model=PaymentModel)
async def get_payment(id: str,
                      payment_service : PaymentService = Depends(get_payment_service),
                      ):
    payment = await payment_service.retrieve_payment(id)
    if payment:
        return payment
    raise HTTPException(status_code=404, detail=f"Pago con ID {id} no encontrado")


@router.put("/{id}", response_description="Actualizar un pago", response_model=PaymentModel)
async def update_payment_data(id: str,
                              payment: PaymentModel,
                              payment_service : PaymentService = Depends(get_payment_service),
                              ):
    payment = {k: v for k, v in payment.model_dump(by_alias=True, exclude_defaults=True, exclude_none=True).items() if v is not None}
    updated_payment = await payment_service.update_payment(id, payment)
    if updated_payment:
        return await payment_service.retrieve_payment(id)
    raise HTTPException(status_code=404, detail=f"Pago con ID {id} no encontrado")


@router.delete("/{id}", response_description="Eliminar un pago")
async def delete_payment_data(id: str,
                              payment_service : PaymentService = Depends(get_payment_service),
                              ):
    deleted_payment = await payment_service.delete_payment(id)
    if deleted_payment:
        return "Pago eliminado"
    raise HTTPException(status_code=404, detail=f"Pago con ID {id} no encontrado")

