from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database
from app.utils.auth import get_current_user

router = APIRouter()

# ✅ Get all mutual funds


@router.get("/mutual-funds", response_model=list[schemas.MutualFundResponse])
def get_mutual_funds(db: Session = Depends(database.get_db)):
    return crud.get_all_mutual_funds(db)

# ✅ Get details of a specific mutual fund


@router.get("/mutual-funds/{fund_id}", response_model=schemas.MutualFundResponse)
def get_fund_details(fund_id: int, db: Session = Depends(database.get_db)):
    fund = crud.get_mutual_fund(db, fund_id)
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    return fund

# ✅ Create new mutual fund (Admin only)


@router.post("/mutual-funds", response_model=schemas.MutualFundResponse)
def create_mutual_fund(fund: schemas.MutualFundBase, db: Session = Depends(database.get_db)):
    return crud.create_mutual_fund(db, fund)

# ✅ Update mutual fund details (Admin)


@router.put("/mutual-funds/{fund_id}", response_model=schemas.MutualFundResponse)
def update_mutual_fund(fund_id: int, fund: schemas.MutualFundBase, db: Session = Depends(database.get_db)):
    return crud.update_mutual_fund(db, fund_id, fund)

# ✅ Delete mutual fund (Admin)


@router.delete("/mutual-funds/{fund_id}")
def delete_mutual_fund(fund_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_mutual_fund(db, fund_id)
