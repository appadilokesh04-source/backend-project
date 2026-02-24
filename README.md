**BabaFly Backend API:**A production-ready E-Commerce Backend System built with FastAPI, PostgreSQL, and SQLAlchemy.
This backend powers the BabaFly platform with secure authentication, product management, categories, orders, filtering, sorting, and role-based access control.

**Tech Stack:**
**Framework:** FastAPI
**Database:** PostgreSQL
**ORM:** SQLAlchemy
**Validation:** Pydantic
**Authentication**: JWT (JSON Web Tokens)
**Password Hashing:** bcrypt
**Architecture:** Clean MVC Structure
**Testing:** Pytest

**Project Structure**
/app
   /routes
   /controllers
   /models
   /schemas
   /services
   /config
   /utils
main.py
requirements.txt
README.md
**Authentication Module (Users)**
**Endpoints**
**Method	Endpoint	Description**
POST	/api/users/register	Register new user
POST	/api/users/login	Login user
GET	/api/users/profile	Get logged-in user profile (JWT Required)

**Features**
JWT-based authentication
Password hashing using bcrypt
Unique email validation
Role-based access (Admin/User)

**Product Module
Endpoints**
**Method	Endpoint	Description**
GET	/api/products	Get all products (Filters + Pagination)
GET	/api/products/{id}	Get product by ID
POST	/api/products	Create product (Admin Only)
PUT	/api/products/{id}	Update product (Admin Only)
DELETE	/api/products/{id}	Delete product (Admin Only)

**Product Fields**
id
name
description
category
price
discount
stock
rating
metalType
polishType
imageUrl
createdAt
updatedAt

**Category Module**
**Endpoints**
**Method	Endpoint	Description**
GET	/api/categories	Get all categories
GET	/api/categories/{id}/products	Get products by category

**Category Fields**
id
name
imageUrl

**Order Module**
**Endpoints
Method	Endpoint	Description**
POST	/api/orders	Create order (JWT Required)
GET	/api/orders	Get user orders
GET	/api/orders/{id}	Get specific order

**Order Fields**
id
userId
items[]
totalPrice
paymentStatus
address
createdAt

**Filtering, Sorting & Pagination
Supported Query Parameters (GET /api/products)**

**Filtering:**
price_min=
price_max=
metal=
polish=

**Sorting:**
sort=latest
sort=price_low
sort=price_high
sort=rating
sort=popularity

**Pagination:**
page=
limit=

**Security Features**
JWT Authentication
Role-Based Authorization (Admin/User)
Password hashing (bcryp
Pydantic input validation
Centralized error handling middleware
Secure environment variables
Request & error logging

**Auto API Documentation**
FastAPI automatically provides Swagger documentation.
After running the server:
http://localhost:8000/docs

**Installation & Setup**
**1️ Clone Repository**
git clone https://github.com/appadilokesh04-source/backend-project.git
cd babafly-backend
**2️ Create Virtual Environmen**t
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
**3️ Install Dependencies**
pip install -r requirements.txt
**4️ Setup Environment Variables**
Create a .env file:
DATABASE_URL=postgresql://user:password@localhost:5432/babafly
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
**5️ Run Server**
uvicorn main:app --reload

**Running Tests**
Minimum 5 automated tests included using Pytest:
User Registration
User Login
Create Product
Fetch Product
Create Order

Run tests:
pytest

**requirements.txt**
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
passlib[bcrypt]
python-jose
pydantic
pytest
httpx

**Architecture Overview**
The project follows clean MVC separation:
**Routes** → API endpoints
**Controllers** → Business logic
**Models** → Database models
**Schemas** → Request/Response validation
**Services** → Reusable logic
**Utils** → Helpers (JWT, hashing, logging)
**Config** → Database & environment config

**Production Readiness**
Clean PEP8 Code
Structured Architecture
Secure Authentication
Role-Based Access
Error Logging
Input Validation
Pagination & Filtering
Automated Testing

**Author**
**Lokesh Appadi**
Backend Developer | FastAPI | PostgreSQL | DevOps Engineer
