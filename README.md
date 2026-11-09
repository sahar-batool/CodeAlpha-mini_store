# Django Mini Store
**Live demo:** https://code-alpha-mini-store-a1dd6ms9k-junior-developer4.vercel.app/
## Deployment

Deployed on Vercel with a Neon Postgres database. Secrets (secret key, email credentials, database address) are set as environment variables and are not stored in the repository.

A basic e-commerce website built with **Django**, **HTML**, **CSS** and **JavaScript**.

## Features

- Product listing with categories, search and pagination
- Product details page with related products
- Session-based shopping cart (add, update, remove) with AJAX add-to-cart
- User registration, login and logout
- Checkout with stock checks and database transactions
- Order history for customers
- Admin panel to manage products, categories and orders (change status, cancel and restock)

## Tech stack

- Backend: Python, Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite

## Getting started

```bash
# 1. Clone the repository
git clone https://github.com/sahar-batool/django-mini-store.git
cd django-mini-store

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows (cmd): venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the database
python manage.py migrate

# 5. Load sample products
python manage.py seed_products

# 6. Create an admin account
python manage.py createsuperuser

# 7. Run the server
python manage.py runserver
```

Open http://127.0.0.1:8000/ for the shop and http://127.0.0.1:8000/admin/ for the admin panel.

## Project structure

```
config/      project settings and main URLs
store/       models, views, cart, forms, admin, seed command
templates/   HTML templates
static/      CSS and JavaScript
```

