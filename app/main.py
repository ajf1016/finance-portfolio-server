from fastapi import FastAPI
from app.routes import auth, fund, portfolio, investment, portfolio
from app.database import engine, Base

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio Dashboard API")

# ✅ Register API Routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(portfolio.router, prefix="/api", tags=["Portfolio"])
app.include_router(fund.router, prefix="/api", tags=["Mutual Funds"])
app.include_router(investment.router, prefix="/api", tags=["Investments"])
