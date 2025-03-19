from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, MutualFund, Investment, FundAllocation, FundOverlap
from app.utils.auth import get_password_hash

# ✅ Function to seed initial data


def seed_database():
    db: Session = SessionLocal()

    try:
        # ✅ Seed Users
        user1 = User(username="john_doe",
                     hashed_password=get_password_hash("password123"))
        user2 = User(username="jane_smith",
                     hashed_password=get_password_hash("securepass"))

        db.add_all([user1, user2])
        db.commit()

        # ✅ Seed Mutual Funds
        mutual_funds = [
            MutualFund(name="ICICI Prudential Bluechip Fund",
                       isin="INF109K016L0"),
            MutualFund(name="HDFC Top 100 Fund", isin="INF179K01YV8"),
            MutualFund(name="SBI Bluechip Fund", isin="INF200K01QX4"),
            MutualFund(name="Axis Bluechip Fund", isin="INF846K01DP8"),
            MutualFund(name="Mirae Asset Large Cap Fund", isin="INF769K01AX2"),
        ]
        db.add_all(mutual_funds)
        db.commit()

        # ✅ Fetch Mutual Fund IDs
        fund_mapping = {
            fund.name: fund.id for fund in db.query(MutualFund).all()}

        # ✅ Seed Investments
        investments = [
            Investment(user_id=user1.id, fund_id=fund_mapping["ICICI Prudential Bluechip Fund"],
                       date="2023-01-10", amount_invested=1000000, nav_at_investment=100, returns_since_investment=12.5),
            Investment(user_id=user1.id, fund_id=fund_mapping["HDFC Top 100 Fund"], date="2022-12-05",
                       amount_invested=800000, nav_at_investment=100, returns_since_investment=10.2),
            Investment(user_id=user2.id, fund_id=fund_mapping["SBI Bluechip Fund"], date="2023-02-15",
                       amount_invested=1200000, nav_at_investment=100, returns_since_investment=11),
            Investment(user_id=user2.id, fund_id=fund_mapping["Axis Bluechip Fund"], date="2022-11-20",
                       amount_invested=950000, nav_at_investment=100, returns_since_investment=9.8),
            Investment(user_id=user1.id, fund_id=fund_mapping["Mirae Asset Large Cap Fund"], date="2023-03-01",
                       amount_invested=1100000, nav_at_investment=100, returns_since_investment=13),
        ]
        db.add_all(investments)
        db.commit()

        # ✅ Seed Fund Allocations (Sectors)
        allocations = [
            FundAllocation(
                fund_id=fund_mapping["ICICI Prudential Bluechip Fund"], sector="IT", percentage=38),
            FundAllocation(
                fund_id=fund_mapping["ICICI Prudential Bluechip Fund"], sector="Financials", percentage=37),
            FundAllocation(
                fund_id=fund_mapping["ICICI Prudential Bluechip Fund"], sector="Energy", percentage=25),

            FundAllocation(
                fund_id=fund_mapping["HDFC Top 100 Fund"], sector="Financials", percentage=80),
            FundAllocation(
                fund_id=fund_mapping["HDFC Top 100 Fund"], sector="Energy", percentage=20),
        ]
        db.add_all(allocations)
        db.commit()

        # ✅ Seed Fund Overlap Data
        overlaps = [
            FundOverlap(fund_id=fund_mapping["ICICI Prudential Bluechip Fund"],
                        overlapping_fund_id=fund_mapping["HDFC Top 100 Fund"], overlap_percentage=67),
            FundOverlap(fund_id=fund_mapping["ICICI Prudential Bluechip Fund"],
                        overlapping_fund_id=fund_mapping["SBI Bluechip Fund"], overlap_percentage=87),
            FundOverlap(fund_id=fund_mapping["ICICI Prudential Bluechip Fund"],
                        overlapping_fund_id=fund_mapping["Axis Bluechip Fund"], overlap_percentage=88),
            FundOverlap(fund_id=fund_mapping["ICICI Prudential Bluechip Fund"],
                        overlapping_fund_id=fund_mapping["Mirae Asset Large Cap Fund"], overlap_percentage=100),
        ]
        db.add_all(overlaps)
        db.commit()

        print("✅ Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")

    finally:
        db.close()


# ✅ Run the seeder
if __name__ == "__main__":
    seed_database()
