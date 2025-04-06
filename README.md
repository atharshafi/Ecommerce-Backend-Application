# E-Commerce Backend API

A robust e-commerce backend built with FastAPI, PostgreSQL, and SQLAlchemy, featuring user authentication, product management, shopping cart functionality, and order processing.

## 📌 Features

- **User Authentication** (JWT tokens)
- **Role-Based Access Control** (Admin/Customer)
- **Product Catalog Management**
- **Shopping Cart System**
- **Order Processing**
- **Automated API Documentation** (Swagger/Redoc)

## 🚀 API Endpoints

### 🔐 Authentication
| Endpoint          | Method | Description                     | Auth Required |
|-------------------|--------|---------------------------------|---------------|
| `/auth/register`  | POST   | Register new user               | No            |
| `/auth/token`     | POST   | Login and get access token      | No            |
| `/auth/me`        | GET    | Get current user details        | Yes           |

### 🛍️ Products
| Endpoint              | Method | Description                     | Auth Required |
|-----------------------|--------|---------------------------------|---------------|
| `/products/`          | GET    | List all products               | No            |
| `/products/`          | POST   | Create new product              | Admin         |
| `/products/{product_id}` | GET  | Get product details             | No            |

### 🛒 Cart
| Endpoint                      | Method | Description                     | Auth Required |
|-------------------------------|--------|---------------------------------|---------------|
| `/cart/`                      | GET    | Get user's cart                 | Yes           |
| `/cart/items/`                | POST   | Add item to cart                | Yes           |
| `/cart/items/{product_id}`    | PUT    | Update item quantity            | Yes           |
| `/cart/items/{product_id}`    | DELETE | Remove item from cart           | Yes           |
| `/cart/clear`                 | DELETE | Clear entire cart               | Yes           |

### 📦 Orders
| Endpoint                      | Method | Description                     | Auth Required |
|-------------------------------|--------|---------------------------------|---------------|
| `/orders/`                    | GET    | List user's orders              | Yes           |
| `/orders/`                    | POST   | Create new order from cart      | Yes           |
| `/orders/{order_id}`          | GET    | Get order details               | Yes           |
| `/orders/{order_id}/cancel`   | POST   | Cancel order                    | Yes           |
| `/orders/{order_id}/items`    | GET    | Get order items                 | Yes           |

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- PDM (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ecommerce-fullstack.git
   cd ecommerce-fullstack/ecommerce-backend
   
2. Install Dependencies:
   ```bash
   pdm install
3. Set up environment variables (create .env file):
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/db_name
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
4. Run database migrations:
   ```bash
   alembic upgrade head
5. Start the server:
   ```bash
   pdm run uvicorn app.main:app --reload
   
# Database Structure

## 📊 Tables Overview

### 1. `users` - User Accounts
| Column            | Type         | Description                          | Constraints              |
|-------------------|--------------|--------------------------------------|--------------------------|
| `id`             | SERIAL       | Primary key                         | PRIMARY KEY              |
| `email`          | VARCHAR(255) | User's email address                | UNIQUE, NOT NULL         |
| `hashed_password`| VARCHAR(255) | BCrypt-hashed password              | NOT NULL                 |
| `is_active`      | BOOLEAN      | Account status (active/inactive)    | DEFAULT TRUE             |
| `role`           | ENUM         | User role (ADMIN/CUSTOMER)          | DEFAULT 'CUSTOMER'       |
| `created_at`     | TIMESTAMP    | Account creation timestamp          | DEFAULT CURRENT_TIMESTAMP|

**Relationships**:
- One-to-many with `carts`
- One-to-many with `orders`

---

### 2. `products` - Product Catalog
| Column        | Type         | Description                     | Constraints              |
|---------------|--------------|---------------------------------|--------------------------|
| `id`         | SERIAL       | Primary key                    | PRIMARY KEY              |
| `name`       | VARCHAR(100) | Product name                   | NOT NULL, UNIQUE         |
| `description`| TEXT         | Detailed product description   |                          |
| `price`      | DECIMAL(10,2)| Product price                  | NOT NULL, CHECK(>0)      |
| `image_url`  | VARCHAR(255) | Product image URL              |                          |
| `category`   | VARCHAR(50)  | Product category               |                          |
| `stock`      | INTEGER      | Available quantity             | DEFAULT 0, CHECK(>=0)    |

**Relationships**:
- One-to-many with `cart_items`
- One-to-many with `order_items`

---

### 3. `carts` - Shopping Carts
| Column     | Type    | Description                     | Constraints              |
|------------|---------|---------------------------------|--------------------------|
| `id`      | SERIAL  | Primary key                    | PRIMARY KEY              |
| `user_id` | INTEGER | Associated user                | FOREIGN KEY (users.id)   |

**Relationships**:
- Many-to-one with `users`
- One-to-many with `cart_items`

---

### 4. `cart_items` - Items in Carts
| Column       | Type    | Description                     | Constraints                     |
|--------------|---------|---------------------------------|---------------------------------|
| `id`        | SERIAL  | Primary key                    | PRIMARY KEY                     |
| `cart_id`   | INTEGER | Parent cart                    | FOREIGN KEY (carts.id)          |
| `product_id`| INTEGER | Product in cart                | FOREIGN KEY (products.id)       |
| `quantity`  | INTEGER | Item quantity                  | NOT NULL, CHECK(quantity > 0)   |

---

### 5. `orders` - Customer Orders
| Column          | Type         | Description                     | Constraints              |
|-----------------|--------------|---------------------------------|--------------------------|
| `id`           | SERIAL       | Primary key                    | PRIMARY KEY              |
| `user_id`      | INTEGER      | Ordering user                  | FOREIGN KEY (users.id)   |
| `total_amount` | DECIMAL(10,2)| Order total                    | NOT NULL, CHECK(>0)      |
| `status`       | VARCHAR(20)  | Order status                   | NOT NULL                 |
| `created_at`   | TIMESTAMP    | Order timestamp                | DEFAULT CURRENT_TIMESTAMP|
| `shipped_at`   | TIMESTAMP    | Shipping timestamp             |                          |

**Status Values**:
- `pending` 
- `processing` 
- `shipped` 
- `delivered` 
- `cancelled`

**Relationships**:
- Many-to-one with `users`
- One-to-many with `order_items`

---

### 6. `order_items` - Items in Orders
| Column            | Type         | Description                     | Constraints              |
|-------------------|--------------|---------------------------------|--------------------------|
| `id`             | SERIAL       | Primary key                    | PRIMARY KEY              |
| `order_id`       | INTEGER      | Parent order                   | FOREIGN KEY (orders.id)  |
| `product_id`     | INTEGER      | Purchased product              | FOREIGN KEY (products.id)|
| `quantity`       | INTEGER      | Item quantity                  | NOT NULL, CHECK(>0)      |
| `price_at_purchase`| DECIMAL(10,2)| Price when ordered             | NOT NULL, CHECK(>0)      |

---

## 🔄 Database Schema Diagram
```mermaid
erDiagram
    users ||--o{ carts : "has"
    users ||--o{ orders : "places"
    carts }o--|| cart_items : "contains"
    products ||--o{ cart_items : "in"
    products ||--o{ order_items : "in"
    orders ||--o{ order_items : "contains"