# 🐔 Poultry Farm Management System

A full-stack Django web application for connecting poultry farmers (sellers) with buyers in Bangladesh.

---

## 🚀 Quick Setup

### 1. Clone / Extract the project
```bash
cd poultry_farm
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure database (SQLite is default — no setup needed)
For **PostgreSQL**, open `poultry_farm/settings.py`, comment out the SQLite block and uncomment the PostgreSQL block, then update credentials.

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create sample data (demo users + products)
```bash
python manage.py create_sample_data
```

### 7. Run the server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 👤 Demo Credentials

| Role   | Email                | Password  |
|--------|----------------------|-----------|
| Admin  | admin@poultry.com    | admin123  |
| Seller | rahim@farm.com       | seller123 |
| Seller | karim@farm.com       | seller123 |
| Seller | fatima@farm.com      | seller123 |
| Buyer  | buyer@test.com       | buyer123  |

**Demo Coupon:** `WELCOME10` — 10% discount on any order above ৳200

---

## ✅ Features

| Feature | Description |
|---------|-------------|
| 👥 User System | Buyer / Seller registration with email uniqueness |
| 🌾 Farm Profile | Sellers create & manage farm page with image |
| 📦 Products | Add/edit/delete products with multiple images |
| 🛒 Cart | Add to cart, increase/decrease quantity, remove |
| 💳 Checkout | bKash/Nagad payment with transaction ID |
| 🎟️ Coupons | Discount coupon system with validation |
| 📋 Orders | Full order lifecycle — Pending → Processing → Delivered |
| 🔔 Notifications | Real-time order & system notifications |
| 💬 Chat | Buyer↔Seller messaging + AI assistant |
| 📱 Social Feed | Farm posts with like, comment, share |
| 🔍 Search | Global product & farm search with category filter |
| ⚙️ Admin Panel | Full admin control over users, farms, orders |

---

## 💳 Payment Info (Merchant)
- **bKash / Nagad:** `01745532992`
- Manual transaction ID entry by buyer
- Admin verifies payment in admin panel

---

## 🗂️ Project Structure

```
poultry_farm/
├── accounts/          # User registration, login, profile
├── farms/             # Farm profiles, farm pages
├── products/          # Product CRUD, categories
├── orders/            # Cart, checkout, order management
├── notifications/     # Order & system notifications
├── social/            # Farm feed, likes, comments
├── chat/              # Buyer-Seller chat + AI assistant
├── templates/         # All HTML templates
├── static/            # CSS, JS, images
├── media/             # User uploaded files
└── poultry_farm/      # Settings, URLs
```

---

## ⚙️ Tech Stack
- **Backend:** Django 4.x (MVT Architecture)
- **Database:** SQLite (dev) / PostgreSQL (production)
- **Frontend:** Bootstrap 5, FontAwesome, Vanilla JS
- **Auth:** Custom AbstractBaseUser with email login
- **Media:** Pillow for image handling
