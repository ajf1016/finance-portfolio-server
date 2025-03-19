from pydantic import BaseModel
from datetime import date
from typing import List, Optional

# User schema


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

# ✅ Schema for a single data point in the graph


class InvestmentHistoryPoint(BaseModel):
    date: date
    value: float

# ✅ Update `/api/portfolio/stock-allocation` response schema


class StockAllocationResponse(BaseModel):
    history: List[InvestmentHistoryPoint]  # ✅ Historical investment values
    total_value: float  # ✅ Latest investment value
    change_amount: float  # ✅ Change in value over selected period
    change_percentage: float  # ✅ Percentage change


# Mutual Fund schema
class MutualFundBase(BaseModel):
    name: str
    isin: str


class MutualFundResponse(MutualFundBase):
    id: int

# Investment schema


class InvestmentBase(BaseModel):
    fund_id: int
    date: date
    amount_invested: float
    nav_at_investment: float
    returns_since_investment: float


class InvestmentResponse(InvestmentBase):
    id: int
    user_id: int

# Fund Allocation schema


class FundAllocationBase(BaseModel):
    fund_id: int
    sector: str
    percentage: float


class FundAllocationResponse(FundAllocationBase):
    id: int

# Overlap schema


class FundOverlapBase(BaseModel):
    fund_id: int
    overlapping_fund_id: int
    overlap_percentage: float


class FundOverlapResponse(FundOverlapBase):
    id: int


class PortfolioOverview(BaseModel):
    initial_investment: float
    current_value: float
    growth_percentage: float
    one_day_return: Optional[float]  # ✅ Add 1-Day Return Field
    best_performing_scheme: Optional[str]
    best_performing_scheme_return: Optional[float]  # ✅ Add Best Fund %
    worst_performing_scheme: Optional[str]
    worst_performing_scheme_return: Optional[float]   # ✅ New field
