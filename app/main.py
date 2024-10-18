from fastapi import FastAPI
from mangum import Mangum

from app.routes import payments, wallets


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(wallets.router, prefix="/wallets", tags=["wallets"])

handler = Mangum(app)
