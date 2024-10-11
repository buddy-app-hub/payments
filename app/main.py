from fastapi import FastAPI

from app.routes import payments, wallets


app = FastAPI()


app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(wallets.router, prefix="/wallets", tags=["wallets"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
