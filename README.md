# 📦 PVZ Management and Product Reception Service

## 📌 Description

This service is designed to manage pickup points (PVZ) and the product reception process.

The system implements the following functionality:

* PVZ creation
* Reception management
* Product addition and deletion
* Role-based access control
* Reception state tracking

The system provides full visibility into PVZ operations and all product reception activities.

---

## 🧱 Architecture

The project follows a layered architecture:

```
Client → API → Service → Repository → Database
```

### Layers:

* **API (FastAPI)**
  Handles HTTP requests, input validation, and dependency injection

* **Service Layer**
  Contains business logic, system rules, and use-case handling

* **Repository Layer**
  Abstracts database access (CRUD operations, queries)

* **Database**
  PostgreSQL / SQLite (used for testing), SQLAlchemy ORM

---

## ⚙️ Technologies

* FastAPI
* SQLAlchemy (Async)
* PostgreSQL / SQLite (for tests)
* Alembic
* JWT (authentication)
* Pytest + HTTPX (testing)

---

## 🔐 Authentication and Roles

JWT-based authentication is used.

### Token contains:

* `sub` — user ID
* `role` — user role

### Roles:

* **moderator**

  * can create PVZ

* **employee**

  * can create receptions
  * can add products
  * can delete products
  * can close receptions

---

## 🧠 Business Logic

### 📍 PVZ

* Creation is allowed only for users with the `moderator` role
* Allowed cities:

  * Moscow
  * Saint Petersburg
  * Kazan
* Attempting to create a PVZ in any other city results in an error

---

### 📦 Product Reception

* Can be created by users with the `employee` role
* Each PVZ can have only one active reception
* Attempting to create a new reception while another is active results in an error

**Statuses:**

* `IN_PROGRESS`
* `CLOSE`

---

### ➕ Adding Products

* Available only for `employee`
* Product is linked to:

  * a PVZ
  * the latest active reception
* If no active reception exists → error

---

### ➖ Deleting Products (LIFO)

* Allowed only for active (not closed) receptions
* Uses the principle:

  * **LIFO (Last In — First Out)**
* The last added product is removed
* Deletion is not allowed after reception is closed

---

### 🔒 Closing a Reception

* Available only for `employee`
* Requires an active reception

After closing:

* adding products is not allowed
* deleting products is not allowed

---

## ⚠️ Consistency and Race Condition Protection

To prevent multiple active receptions:

* validation is implemented at the service layer
* it is recommended to enforce a database-level constraint (unique constraint):

```
one pvz_id → only one IN_PROGRESS
```

---

## 📡 API Endpoints

### Auth

* `POST /api/user/register`
* `POST /api/user/login`
* `POST /api/user/refresh`
* `POST /api/user/dummyLogin`

### PVZ

* `POST /api/pvz/create`

### Reception

* `POST /api/reception/create`
* `PUT /api/reception/close_reception/pvz/{pvz_id}`

### Product

* `POST /api/product/create`
* `DELETE /api/product/pvz/{pvz_id}/delete`

---

## 🧪 Testing

Used tools:

* pytest
* httpx.AsyncClient
* separate test database (SQLite)

### Coverage:

* registration and authentication
* PVZ creation
* role validation (403)
* reception creation
* prevention of duplicate receptions
* product addition
* product deletion (LIFO)
* reception closing

---

## 🗄️ Database

* ORM: SQLAlchemy (async)
* Migrations: Alembic

---

## 📜 Logging

Standard `logging` is used.

Logged events:

* HTTP requests
* errors
* key business events:

  * PVZ creation
  * reception creation
  * product addition

---

## 🚀 Running the Project

```bash
git clone <repo>

python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

pip install -r requirements.txt

uvicorn src.main:app --reload
```

## Running with Docker

```bash
docker compose up --build
```

## Stop

```bash
docker compose down -v
```

## 🧪 Running Tests

```bash
pytest -vv
```

---

## 📌 Additional Notes

The project implements:

* strict role-based access control
* separation of business logic
* asynchronous database interaction
* testable architecture

---

## 📎 Assignment Link

[https://github.com/avito-tech/tech-internship/blob/main/Tech%20Internships/Backend/Backend-trainee-assignment-spring-2025/Backend-trainee-assignment-spring-2025.md](https://github.com/avito-tech/tech-internship/blob/main/Tech%20Internships/Backend/Backend-trainee-assignment-spring-2025/Backend-trainee-assignment-spring-2025.md)

---

## 📊 Summary

The service covers core requirements:

* PVZ management
* product reception control
* business logic constraints
* protection against inconsistent states
* logging
* API testing
