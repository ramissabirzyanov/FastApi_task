import uvicorn
from fastapi import FastAPI
from app.wallet.endpoints import router as wallet_router
app = FastAPI()
app.include_router(wallet_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
