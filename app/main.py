from fastapi import FastAPI
from app.routes import auth, fund, portfolio, investment, portfolio
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import os

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio Dashboard API")

#  Enable CORS (Fixes frontend communication issues)
app.add_middleware(
    CORSMiddleware,
    #  Replace with your frontend domain
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)

#  Register API Routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(portfolio.router, prefix="/api", tags=["Portfolio"])
app.include_router(fund.router, prefix="/api", tags=["Mutual Funds"])
app.include_router(investment.router, prefix="/api", tags=["Investments"])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Fallback to 8000 if no port is set
    uvicorn.run("main:app", host="0.0.0.0", port=port)
