from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Index
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class MutualFund(Base):
    __tablename__ = "mutual_funds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    isin = Column(String, unique=True)

    investments = relationship("Investment", back_populates="fund")
    allocations = relationship("FundAllocation", back_populates="fund")

    #  Explicitly define `foreign_keys` in the relationship
    overlaps = relationship(
        "FundOverlap",
        # Explicitly defining fund_id as the foreign key
        foreign_keys="[FundOverlap.fund_id]",
        back_populates="fund"
    )


class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"))
    date = Column(Date)
    amount_invested = Column(Float)
    nav_at_investment = Column(Float)
    returns_since_investment = Column(Float)

    user = relationship("User")
    fund = relationship("MutualFund", back_populates="investments")


class FundAllocation(Base):
    __tablename__ = "fund_allocations"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"))
    sector = Column(String)
    percentage = Column(Float)

    fund = relationship("MutualFund", back_populates="allocations")


class FundOverlap(Base):
    __tablename__ = "fund_overlaps"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"))
    overlapping_fund_id = Column(Integer, ForeignKey("mutual_funds.id"))
    overlap_percentage = Column(Float)

    #  Explicitly define `foreign_keys` in the relationships
    fund = relationship("MutualFund", foreign_keys=[
                        fund_id], back_populates="overlaps")
    overlapping_fund = relationship(
        "MutualFund", foreign_keys=[overlapping_fund_id])


# Indexing for optimization
Index("idx_fund_isin", MutualFund.isin)
Index("idx_fund_overlap", FundOverlap.fund_id, FundOverlap.overlapping_fund_id)
