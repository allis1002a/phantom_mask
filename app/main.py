from fastapi import FastAPI
from app.routers import pharmacies, users, search, transactions

app = FastAPI()

app.include_router(pharmacies.router, prefix="/pharmacies", tags=["Pharmacies"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(transactions.router,prefix="/transactions", tags=["Transactions"])
