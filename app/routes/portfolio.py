from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, database
from app.utils.auth import get_current_user

router = APIRouter()

# ✅ Get portfolio overview


@router.get("/portfolio", response_model=schemas.PortfolioOverview)
def get_portfolio(db: Session = Depends(database.get_db), user: dict = Depends(get_current_user)):
    return crud.get_portfolio(db, user["username"])

# ✅ Get sector allocation


@router.get("/portfolio/sector-allocation")
def get_sector_allocation(db: Session = Depends(database.get_db), user: dict = Depends(get_current_user)):
    return crud.get_sector_allocation(db, user["username"])

# ✅ Get stock allocation


@router.get("/portfolio/stock-allocation")
def get_stock_allocation(db: Session = Depends(database.get_db), user: dict = Depends(get_current_user)):
    return crud.get_stock_allocation(db, user["username"])

# ✅ Get overlap analysis


@router.get("/portfolio/overlap")
def get_fund_overlap(db: Session = Depends(database.get_db), user: dict = Depends(get_current_user)):
    return crud.get_fund_overlap(db, user["username"])
