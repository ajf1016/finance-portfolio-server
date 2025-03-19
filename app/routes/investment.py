from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database
from app.utils.auth import get_current_user

router = APIRouter()

# ✅ Create new investment


@router.post("/investments", response_model=schemas.InvestmentResponse)
def create_investment(investment: schemas.InvestmentBase, db: Session = Depends(database.get_db), user: dict = Depends(get_current_user)):
    return crud.create_investment(db, user["username"], investment)

# ✅ Get all investments of a user


@router.get("/investments", response_model=list[schemas.InvestmentResponse])
def get_investments(db: Session = Depends(database.get_db), user: dict = Depends(get_current_user)):
    return crud.get_user_investments(db, user["username"])
