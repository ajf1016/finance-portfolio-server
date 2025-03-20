# 📊 Portfolio Dashboard Backend (FastAPI)
**Investment & Mutual Fund Analysis API with Authentication & Authorization**

## 🚀 Project Overview
This is the backend for a **Portfolio Dashboard** that helps users track and analyze their **mutual fund investments**.  
It provides **investment insights, sector allocations, stock allocations, and fund overlap analysis**.

The backend is built with **FastAPI**, using **PostgreSQL** as the database, and follows **RESTful API best practices** with authentication & authorization.

---

## 🏗 Tech Stack
| Technology                | Usage                                    |
|---------------------------|------------------------------------------|
| **FastAPI**               | Web framework for building APIs          |
| **PostgreSQL**            | Database to store investment data        |
| **SQLAlchemy**            | ORM for database interactions            |
| **Alembic**               | Database migrations                      |
| **JWT (JSON Web Tokens)** | Secure authentication                    |

---

## 📌 Features Implemented
### 🔹 User Authentication & Authorization
- **User Signup & Login** with **hashed passwords**
- **JWT-based authentication** for secure API access
- **Token validation middleware** for protected routes

### 🔹 Investment Dashboard
- **Investment summary** (initial investment, current value, growth %)
- **Sector-wise allocation of investments**
- **Stock-wise allocation for funds**
- **Overlap analysis of funds** (common stocks, % overlap)

### 🔹 Optimized APIs
- **Indexed queries** for faster retrieval
- **CORS enabled** for frontend communication
- **Error handling & logging** for stability

---

## ⚙️ Setup Instructions
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/portfolio-dashboard-backend.git
cd portfolio-dashboard-backend
```
2️⃣ Create & Activate Virtual Environment

python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate  # For Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Set Up PostgreSQL Database

    Install PostgreSQL if not already installed.
    Create a new database:

CREATE DATABASE portfolio_db;

    Update .env file with DB credentials:

DATABASE_URL=postgresql://username:password@localhost/portfolio_db
SECRET_KEY=supersecretkey

5️⃣ Run Database Migrations

alembic upgrade head

6️⃣ Start FastAPI Server

uvicorn app.main:app --reload

🚀 API is now running at http://localhost:8000/docs
🔐 Authentication & Authorization

This API uses JWT-based authentication.
1️⃣ User Signup

Endpoint: POST /auth/signup
Body:

{
    "username": "testuser",
    "password": "securepassword"
}

2️⃣ User Login

Endpoint: POST /auth/login
Body:

{
    "username": "testuser",
    "password": "securepassword"
}

Response:

{
    "access_token": "your_jwt_token"
}

Use this token in the Authorization header for protected routes:

Authorization: Bearer your_jwt_token

## 🔗 API Endpoints
** User Authentication
 - Method	Endpoint	Description
 - POST	/auth/signup	Register a new user
 - POST	/auth/login	Login and get JWT token
** Portfolio Overview
 - Method	Endpoint	Description
 - GET	/api/portfolio	Get portfolio overview
 - GET	/api/portfolio/sector-allocation	Get sector allocation
 - GET	/api/portfolio/stock-allocation?period=1M	Get stock allocation (1M, 3M, 6M, etc.)
 - GET	/api/portfolio/overlap	Get overlap analysis of funds
** Mutual Funds
 - Method	Endpoint	Description
 - GET	/api/mutual-funds	Get all mutual funds
 - GET	/api/mutual-funds/{fund_id}	Get fund details
 - POST	/api/mutual-funds	Add a new mutual fund (Admin)
 - PUT	/api/mutual-funds/{fund_id}	Update fund details (Admin)
 - DELETE	/api/mutual-funds/{fund_id}	Delete a fund (Admin)
** Investments
 - Method	Endpoint	Description
 - POST	/api/investments	Add new investment
 - GET	/api/investments	Get user investments

## 🛠 Database Schema

The PostgreSQL database schema includes:
🔹 Users Table
```Column	Type	Description
id	INTEGER	Primary key
username	TEXT	Unique username
hashed_password	TEXT	Encrypted password
```
🔹 Mutual Funds Table
```Column	Type	Description
id	INTEGER	Primary key
name	TEXT	Mutual fund name
isin	TEXT	Unique fund identifier
```
🔹 Investments Table
```Column	Type	Description
id	INTEGER	Primary key
user_id	INTEGER	Foreign key (Users)
fund_id	INTEGER	Foreign key (Mutual Funds)
date	DATE	Investment date
amount_invested	FLOAT	Amount invested
returns_since_investment	FLOAT	% returns
```
🔹 Fund Allocations Table
```Column	Type	Description
id	INTEGER	Primary key
fund_id	INTEGER	Foreign key (Mutual Funds)
sector	TEXT	Sector type
percentage	FLOAT	Allocation %
```
🔹 Fund Overlaps Table
```Column	Type	Description
id	INTEGER	Primary key
fund_id	INTEGER	Foreign key (Mutual Funds)
overlapping_fund_id	INTEGER	Foreign key (Mutual Funds)
overlap_percentage	FLOAT	Overlap %
```
