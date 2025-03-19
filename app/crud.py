from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verify password


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create User
# ✅ Create User (Make sure this function exists!)


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get Portfolio Overview


def get_portfolio(db: Session, username: str):
    user = db.query(models.User).filter(
        models.User.username == username).first()

    if not user:
        return {"error": "User not found"}

    investments = db.query(models.Investment).filter(
        models.Investment.user_id == user.id).all()

    if not investments:  # Handle case when user has no investments
        return {
            "initial_investment": 0,
            "current_value": 0,
            "growth_percentage": 0  # No investments → No growth percentage
        }

    total_investment = sum(inv.amount_invested for inv in investments)
    total_current_value = sum(
        inv.amount_invested * (1 + inv.returns_since_investment / 100) for inv in investments)

    growth_percentage = 0 if total_investment == 0 else (
        (total_current_value - total_investment) / total_investment) * 100

    return {
        "initial_investment": total_investment,
        "current_value": total_current_value,
        "growth_percentage": growth_percentage  # Avoid division by zero
    }


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Get all mutual funds


def get_all_mutual_funds(db: Session):
    return db.query(models.MutualFund).all()

# ✅ Get details of a mutual fund


def get_mutual_fund(db: Session, fund_id: int):
    return db.query(models.MutualFund).filter(models.MutualFund.id == fund_id).first()

# ✅ Create new mutual fund


def create_mutual_fund(db: Session, fund: schemas.MutualFundBase):
    new_fund = models.MutualFund(name=fund.name, isin=fund.isin)
    db.add(new_fund)
    db.commit()
    db.refresh(new_fund)
    return new_fund

# ✅ Update mutual fund details


def update_mutual_fund(db: Session, fund_id: int, fund: schemas.MutualFundBase):
    db_fund = db.query(models.MutualFund).filter(
        models.MutualFund.id == fund_id).first()
    if not db_fund:
        return None
    db_fund.name = fund.name
    db_fund.isin = fund.isin
    db.commit()
    db.refresh(db_fund)
    return db_fund

# ✅ Delete mutual fund


def delete_mutual_fund(db: Session, fund_id: int):
    db_fund = db.query(models.MutualFund).filter(
        models.MutualFund.id == fund_id).first()
    if not db_fund:
        return None
    db.delete(db_fund)
    db.commit()
    return {"message": "Mutual fund deleted"}

# ✅ Create a new investment


def create_investment(db: Session, username: str, investment: schemas.InvestmentBase):
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if not user:
        return {"error": "User not found"}

    new_investment = models.Investment(
        user_id=user.id,
        fund_id=investment.fund_id,
        date=investment.date,
        amount_invested=investment.amount_invested,
        nav_at_investment=investment.nav_at_investment,
        returns_since_investment=investment.returns_since_investment
    )

    db.add(new_investment)
    db.commit()
    db.refresh(new_investment)
    return new_investment

# ✅ Get user investments


def get_user_investments(db: Session, username: str):
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if not user:
        return []
    return db.query(models.Investment).filter(models.Investment.user_id == user.id).all()

# ✅ Get sector allocation


def get_sector_allocation(db: Session, username: str):
    return db.query(models.FundAllocation).all()

# ✅ Get stock allocation


def get_stock_allocation(db: Session, username: str):
    return {"message": "Stock allocation API is pending implementation"}

# ✅ Get fund overlap analysis


def get_fund_overlap(db: Session, username: str):
    return db.query(models.FundOverlap).all()
