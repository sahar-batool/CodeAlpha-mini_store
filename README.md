# Django Mini Store

A full-featured e-commerce website built with **Django**, **HTML**, **CSS** and **JavaScript**, deployed on Vercel.

**Live demo:** https://code-alpha-mini-store.vercel.app/

## Features

- Home page with an animated hero, rotating product collage, category tiles and new arrivals
- Product listing with categories, search and pagination
- Product details page with related products and a quantity stepper
- Session-based shopping cart (add, update, remove) with add-to-cart that works without a page reload
- User registration, login and logout
- Password reset by email, with 15-minute links and rate limiting
- Checkout with stock checks inside a database transaction
- Order history for customers, with colored status labels
- Admin panel to manage products, categories and orders (change status, cancel and restock)
- Responsive layout, keyboard-friendly navigation and reduced-motion support

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Django 6.1 |
| Frontend | HTML, CSS, vanilla JavaScript (Google Fonts: Bricolage Grotesque and Figtree) |
| Database | SQLite for local development, PostgreSQL (Neon) in production |
| Email | SMTP (Gmail app password) |
| Hosting | Vercel (serverless functions, static files served from its CDN) |
| Config | Environment variables, `python-dotenv` for local development |

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

# 4. Create the local database (SQLite)
python manage.py migrate

# 5. Load sample products
python manage.py seed_products

# 6. Create an admin account
python manage.py createsuperuser

# 7. Run the server
python manage.py runserver
```

Open http://127.0.0.1:8000/ for the shop and http://127.0.0.1:8000/admin/ for the admin panel.

### Optional: real emails locally

Create a `.env` file next to `manage.py` (it is ignored by Git):

```
EMAIL_HOST_USER=yourname@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
```

Without it, emails (such as password reset links) are printed in the terminal instead.

## Project structure

```
config/      project settings and main URLs
store/       models, views, cart, forms, admin, rate limiting, seed command
templates/   HTML templates
static/      CSS and JavaScript
```

## Security notes

- Secrets (secret key, database address, email credentials) are read from environment variables and are not stored in the repository.
- Debug mode is off in production, and cookies are marked secure when served over HTTPS.
- Password reset links expire after 15 minutes and work once. Reset requests are limited per email address and per IP address, and the form never reveals whether an account exists.
- Customers can only view their own orders, and prices are always read from the database, never from the browser.

## Deployment

The site is deployed on Vercel, with a Neon PostgreSQL database. Vercel detects the Django project from `manage.py`, runs `collectstatic` during the build and serves static files from its CDN. The database address, secret key and email credentials are set as environment variables in the Vercel project, and every push to `main` redeploys the site.

After the first deployment, the tables and sample data were created by running `migrate` and `seed_products` against the production database from a local terminal.

## Notes

- Product images use image URLs set in the admin or in the seed command.
- Local and production databases are separate: data created in one does not appear in the other.