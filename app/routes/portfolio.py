from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, database
from app.utils.auth import get_current_user

router = APIRouter()

#  Get portfolio overview


@router.get("/portfolio", response_model=schemas.PortfolioOverview)
def get_portfolio(db: Session = Depends(database.get_db), user: dict = Depends(get_current_user)):
    return crud.get_portfolio(db, user["username"])

#  Get sector allocation


@router.get("/portfolio/sector-allocation", response_model=schemas.SectorAllocationResponse)
def get_sector_allocation(
    db: Session = Depends(database.get_db),
    user: dict = Depends(get_current_user)
):
    return crud.get_sector_allocation(db, user["username"])

#  Get stock allocation


@router.get("/portfolio/stock-allocation", response_model=schemas.StockAllocationResponse)
def get_stock_allocation(
    period: str = "1M",  # Accepts "1M", "3M", "6M", "1Y", "3Y", "MAX"
    db: Session = Depends(database.get_db),
    user: dict = Depends(get_current_user)
):
    return crud.get_stock_allocation(db, user["username"], period)

#  Get overlap analysis


@router.get("/portfolio/overlap", response_model=schemas.FundOverlapResponse)
def get_fund_overlap(
    db: Session = Depends(database.get_db),
    user: dict = Depends(get_current_user)
):
    return crud.get_fund_overlap(db, user["username"])
