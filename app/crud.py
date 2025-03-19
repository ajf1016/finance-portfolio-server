from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verify password


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create User


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

    if not investments:
        return {
            "initial_investment": 0,
            "current_value": 0,
            "growth_percentage": 0,
            "one_day_return": 0,
            "best_performing_scheme": None,
            "best_performing_scheme_return": None,
            "worst_performing_scheme": None,
            "worst_performing_scheme_return": None
        }

    #  Total investment and current value
    total_investment = sum(inv.amount_invested for inv in investments)
    total_current_value = sum(
        inv.amount_invested * (1 + inv.returns_since_investment / 100) for inv in investments)
    growth_percentage = ((total_current_value - total_investment) /
                         total_investment) * 100 if total_investment else 0

    #  Find best and worst performing schemes
    best_fund = max(
        investments, key=lambda inv: inv.returns_since_investment, default=None)
    worst_fund = min(
        investments, key=lambda inv: inv.returns_since_investment, default=None)

    best_scheme_name = best_fund.fund.name if best_fund else None
    best_scheme_return = best_fund.returns_since_investment if best_fund else None

    worst_scheme_name = worst_fund.fund.name if worst_fund else None
    worst_scheme_return = worst_fund.returns_since_investment if worst_fund else None

    #  Calculate 1-Day Return
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_investments = db.query(models.Investment).filter(
        models.Investment.user_id == user.id, models.Investment.date <= yesterday.date()
    ).all()

    yesterday_value = sum(inv.amount_invested * (1 + inv.returns_since_investment / 100)
                          for inv in yesterday_investments)
    one_day_return = ((total_current_value - yesterday_value) /
                      yesterday_value) * 100 if yesterday_value else 0

    return {
        "initial_investment": total_investment,
        "current_value": total_current_value,
        "growth_percentage": growth_percentage,
        #  Round to 2 decimal places
        "one_day_return": round(one_day_return, 2),
        "best_performing_scheme": best_scheme_name,
        "best_performing_scheme_return": round(best_scheme_return, 2) if best_scheme_return is not None else None,
        "worst_performing_scheme": worst_scheme_name,
        "worst_performing_scheme_return": round(worst_scheme_return, 2) if worst_scheme_return is not None else None
    }


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#  Get all mutual funds


def get_all_mutual_funds(db: Session):
    return db.query(models.MutualFund).all()

#  Get details of a mutual fund


def get_mutual_fund(db: Session, fund_id: int):
    return db.query(models.MutualFund).filter(models.MutualFund.id == fund_id).first()

#  Create new mutual fund


def create_mutual_fund(db: Session, fund: schemas.MutualFundBase):
    new_fund = models.MutualFund(name=fund.name, isin=fund.isin)
    db.add(new_fund)
    db.commit()
    db.refresh(new_fund)
    return new_fund

#  Update mutual fund details


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

#  Delete mutual fund


def delete_mutual_fund(db: Session, fund_id: int):
    db_fund = db.query(models.MutualFund).filter(
        models.MutualFund.id == fund_id).first()
    if not db_fund:
        return None
    db.delete(db_fund)
    db.commit()
    return {"message": "Mutual fund deleted"}

#  Create a new investment


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

#  Get user investments


def get_user_investments(db: Session, username: str):
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if not user:
        return []
    return db.query(models.Investment).filter(models.Investment.user_id == user.id).all()


#  Get stock allocation
def get_stock_allocation(db: Session, username: str, period: str = "1M"):
    """
    Fetch investment value history and filter based on the selected time range.
    """
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if not user:
        return {"error": "User not found"}

    #  Define period ranges
    period_map = {
        "1M": timedelta(days=30),
        "3M": timedelta(days=90),
        "6M": timedelta(days=180),
        "1Y": timedelta(days=365),
        "3Y": timedelta(days=1095),
        "MAX": timedelta(days=3650)  # Approx 10 years
    }

    #  Get start date based on selected period
    end_date = datetime.now().date()
    start_date = end_date - \
        period_map.get(period, timedelta(days=30))  # Default to 1M

    #  Fetch historical investments
    history = db.query(models.Investment).filter(
        models.Investment.user_id == user.id,
        models.Investment.date >= start_date
    ).order_by(models.Investment.date).all()

    #  Format data points for the graph
    history_points = [
        {"date": inv.date, "value": inv.amount_invested *
            (1 + inv.returns_since_investment / 100)}
        for inv in history
    ]

    #  Calculate latest value and change percentage
    latest_value = history_points[-1]["value"] if history_points else 0
    initial_value = history_points[0]["value"] if history_points else 0
    change_amount = latest_value - initial_value
    change_percentage = (change_amount / initial_value *
                         100) if initial_value else 0

    return {
        "history": history_points,
        "total_value": latest_value,
        "change_amount": change_amount,
        "change_percentage": round(change_percentage, 2)
    }

#  Get fund overlap analysis


def get_fund_overlap(db: Session, username: str):
    """
    Fetch mutual fund overlap data for a user.
    """
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if not user:
        return {"error": "User not found"}

    # ✅ Fetch all investments for the user
    investments = db.query(models.Investment).filter(
        models.Investment.user_id == user.id).all()

    if not investments:
        return {"overlaps": []}

    # ✅ Fetch fund overlap data
    overlap_data = db.query(models.FundOverlap).all()

    response_data = []

    for overlap in overlap_data:
        fund_1 = db.query(models.MutualFund).filter(
            models.MutualFund.id == overlap.fund_id).first()
        fund_2 = db.query(models.MutualFund).filter(
            models.MutualFund.id == overlap.overlapping_fund_id).first()

        if not fund_1 or not fund_2:
            continue

        # ✅ Fetch stocks common to both funds
        fund_1_stocks = db.query(models.FundAllocation).filter(
            models.FundAllocation.fund_id == fund_1.id).all()
        fund_2_stocks = db.query(models.FundAllocation).filter(
            models.FundAllocation.fund_id == fund_2.id).all()

        common_stocks = list(set([s.sector for s in fund_1_stocks]) & set(
            [s.sector for s in fund_2_stocks]))

        response_data.append({
            "fund_name": fund_1.name,
            "overlapping_fund_name": fund_2.name,
            "overlap_percentage": overlap.overlap_percentage,
            "common_stocks": common_stocks
        })

    return {"overlaps": response_data}


#  Get sector allocation
def get_sector_allocation(db: Session, username: str):
    """
    Fetch sector-wise investment allocation for a user.
    """
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if not user:
        return {"error": "User not found"}

    #  Fetch all investments for the user
    investments = db.query(models.Investment).filter(
        models.Investment.user_id == user.id).all()

    if not investments:
        return {"allocations": [], "total_investment": 0}

    #  Map investments to sectors
    sector_investments = {}
    total_investment = 0

    for inv in investments:
        fund = db.query(models.MutualFund).filter(
            models.MutualFund.id == inv.fund_id).first()
        if not fund:
            continue

        #  Fetch sector allocations for this mutual fund
        sector_allocations = db.query(models.FundAllocation).filter(
            models.FundAllocation.fund_id == fund.id).all()

        for allocation in sector_allocations:
            sector_investments[allocation.sector] = sector_investments.get(
                allocation.sector, 0) + (inv.amount_invested * (allocation.percentage / 100))
            total_investment += inv.amount_invested * \
                (allocation.percentage / 100)

    #  Convert data to structured format
    sector_data = [
        {
            "sector": sector,
            "invested_amount": round(amount, 2),
            "percentage": round((amount / total_investment) * 100, 2) if total_investment else 0
        }
        for sector, amount in sector_investments.items()
    ]

    return {
        "allocations": sector_data,
        "total_investment": round(total_investment, 2)
    }
