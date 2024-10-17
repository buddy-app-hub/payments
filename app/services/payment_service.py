from mercadopago import SDK
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

from app.models.payment_model import PaymentModel


class PaymentService:
    BASE_PRODUCT: str = "Buddy"

    def __init__(self, mercado_pago : SDK, payments_collection : AsyncIOMotorCollection) -> None:
        self.sdk = mercado_pago
        self.payments_collection = payments_collection

    def handshake(
        self,
        connection_id: str,
    ) -> str:
        preference_data = {
            "items": [
                {
                "id": "Buddy",
                "title": self.BASE_PRODUCT,
                "description": "Encontrá tu Buddy ideal",
                # "picture_url": "http://www.myapp.com/myimage.jpg",
                # "category_id": "car_electronics",
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": 5000,
                }
            ],
            "back_urls": {
                "success": f"https://backend.buddyapp.link/payments/success?connection_id={connection_id}",
                "pending": f"https://backend.buddyapp.link/payments/pending?connection_id={connection_id}",
                "failure": f"https://backend.buddyapp.link/payments/failure?connection_id={connection_id}",
            },
            "notification_url": "http://notificationurl.com",
            "auto_return": "approved",
            "statement_descriptor": "Buddy",
            # "external_reference": "1643827245",
            # "expires": False,
            # "expiration_date_from": "2022-11-17T09:37:52.000-04:00",
            # "expiration_date_to": "2022-11-17T10:37:52.000-05:00",
            # "marketplace": "NONE",
            # "marketplace_fee": 0,
        }

        preference_response = self.sdk.preference().create(preference_data)
        return preference_response["response"]
    
    async def retrieve_payments(self):
        payments = []
        async for payment in self.payments_collection.find():
            payments.append(PaymentModel(**payment))
        return payments

    async def add_payment(self, payment_data: dict) -> PaymentModel:
        payment = await self.payments_collection.insert_one(payment_data)
        new_payment = await self.payments_collection.find_one({"_id": payment.inserted_id})
        return PaymentModel(**new_payment)

    async def retrieve_payment(self, id: str) -> PaymentModel:
        payment = await self.payments_collection.find_one({"_id": ObjectId(id)})
        if payment:
            return PaymentModel(**payment)

    async def update_payment(self, id: str, data: dict):
        if len(data) < 1:
            return False
        payment = await self.payments_collection.find_one({"_id": ObjectId(id)})
        if payment:
            updated_payment = await self.payments_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": data}
            )
            if updated_payment:
                return True
        return False

    async def delete_payment(self, id: str):
        payment = await self.payments_collection.find_one({"_id": ObjectId(id)})
        if payment:
            await self.payments_collection.delete_one({"_id": ObjectId(id)})
            return True