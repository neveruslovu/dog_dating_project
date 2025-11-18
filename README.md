# DogDating - Django Dog Dating Platform

![DogDating Logo](https://img.shields.io/badge/DogDating-🐕-blue?style=for-the-badge)
![Django Version](https://img.shields.io/badge/Django-4.2+-green?style=flat-square)
![Python Version](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

DogDating is a modern web application built with Django that helps dog owners find compatible companions for their pets. The platform features user profiles, a matching system, favorites, and a responsive design with Russian language support.

---

## 🌟 Features

### Core Functionality

- **User Authentication System** – registration, login, password management
- **Dog Profile Management** – create, edit, and manage multiple dog profiles
- **Matching System** – compatibility matching between dogs
- **Favorites System** – save dogs you’re interested in
- **Match Management** – view and manage match requests
- **User Profiles** – extended user information with avatars
- **Search & Browse** – view all dogs with filtering
- **Dashboard** – central hub for user activities
- **Guest Menu System** – navigation for non‑authenticated users

### Additional Features

- **Russian Language Interface** – `LANGUAGE_CODE='ru-ru'`
- **Menu Management System** – dynamic menu via `menu_app`
- **Custom Error Pages** – 404 and 500 error handling
- **Template Components** – reusable template components
- **Image Validation & Optimization** – validation for dog photos + utilities for placeholders/optimization
- **Management Commands** – data population and menu setup commands

### Technical Features

- **Django 4.2+** – modern Django framework
- **SQLite (dev) + Postgres (prod)**
  - SQLite is used by default for local development.
  - Postgres is used via `DATABASE_URL` (e.g. in Docker/docker‑compose).
- **Settings Package**
  - `project/settings/base.py` – shared configuration
  - `project/settings/development.py` – local/dev overrides
  - `project/settings/production.py` – production settings (security, Postgres)
- **Env‑based configuration** using `django-environ` and `.env`
- **Template System** – Django templates with custom template tags
- **Static & Media Files** – organized static and media handling
- **Logging** – structured console logging suitable for Docker
- **Admin Panel** – Django admin interface

### UI/UX Features

- **Responsive Design** – mobile‑first layout
- **Mobile Optimized** – tested on phones, tablets
- **Dark/Light Theme** – automatic theme switching based on OS
- **Component-based Templates** – header, footer, guest menu, messages
- **Touch-Friendly** – larger hit targets and mobile CSS/JS

---

## 📱 Mobile Support

The project is optimized for mobile devices:

- Responsive grid system (320px–1920px+)
- Touch‑friendly interface (≥48×48 px targets)
- Notch support with safe‑area insets (iOS/Android)
- Portrait/landscape handling
- Optimized images and lazy loading

See:

- [MOBILE_OPTIMIZATION.md](./MOBILE_OPTIMIZATION.md)
- [MOBILE_TESTING_GUIDE.md](./MOBILE_TESTING_GUIDE.md)

---

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Testing](#-testing)
- [Docker & Postgres](#-docker--postgres)
- [Deployment](#-deployment)
- [Roadmap](#-roadmap)

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher (3.11 recommended)
- `pip`
- Virtual environment (recommended)
- Optional: Docker & Docker Compose (for Postgres setup)

### Local Setup (SQLite + venv)

```bash
git clone https://github.com/yourusername/dog-dating.git
cd dog-dating

python -m venv venv
source venv/bin/activate  # Windows PowerShell: .\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
# Edit .env to set SECRET_KEY, DEBUG, DATABASE_URL (optional), email, security, etc.
```

Apply migrations and (optionally) load demo data:

```bash
python manage.py migrate
python manage.py setup_menus      # create navigation menus
python manage.py populate_data    # create demo users, dogs, matches, favorites
```

Create a superuser (optional):

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Access:

- Main site: <http://127.0.0.1:8000>
- Admin: <http://127.0.0.1:8000/admin>

---

## ⚙️ Configuration

### Settings Architecture

The project uses a **settings package** instead of a single `settings.py`:

- `project/settings/base.py`
  - Core application list, middleware, templates, static/media paths.
  - Env‑driven security and database config using `django-environ`.
- `project/settings/development.py`
  - Imports `base` and sets `DEBUG=True` by default.
- `project/settings/production.py`
  - Imports `base`, forces `DEBUG=False` and enables security flags:
    - `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`
    - `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD`
    - `SECURE_SSL_REDIRECT`, `CSRF_TRUSTED_ORIGINS`

Django entrypoints (`manage.py`, `asgi.py`, `wsgi.py`) use:

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
```

which resolves to `project.settings.development` by default.

### Environment Variables (.env)

Core variables (see `.env.example`):

- `SECRET_KEY` – secret key for Django
- `DEBUG` – `True`/`False`
- `ALLOWED_HOSTS` – comma‑separated list
- `DATABASE_URL` – for Postgres or alternative DB, e.g.
  - `sqlite:///project/db.sqlite3` (default fallback)
  - `postgres://user:password@host:5432/dbname`
- Email configuration: `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `EMAIL_USE_SSL`, `DEFAULT_FROM_EMAIL`
- Security flags for production: `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`, `SECURE_SSL_REDIRECT`, `CSRF_TRUSTED_ORIGINS`
- Placeholders for S3/MinIO (not wired yet): `AWS_*`, `MINIO_*`

### Media Files

- Dog photos: `media/dogs/`
- User avatars: `media/avatars/`

Images are validated on upload:

- Allowed types: JPEG, PNG, WebP
- Max size: 5 MB (configurable in code)

---

## 📖 Usage

### Getting Started

1. Register an account.
2. Create one or more dog profiles.
3. Browse the list of dogs, filter, and send match requests.
4. Add dogs to favorites and manage matches.

### User Roles

**Regular Users** can:

- Create and manage dog profiles.
- Browse other dogs.
- Send and receive match requests.
- Manage favorites.

**Administrators** can:

- Access Django admin.
- Manage users, dogs, and menu entries.
- Moderate content.

---

## 📁 Project Structure (Updated)

```text
c:\...\dog_dating_project/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   ├── wsgi.py
│   └── settings/
│       ├── __init__.py          # exports development settings by default
│       ├── base.py              # shared settings (env‑driven)
│       ├── development.py       # dev overrides
│       └── production.py        # production overrides (security, Postgres)
├── dogs/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│   ├── views_new.py
│   ├── management/
│   │   └── commands/
│   │       └── populate_data.py
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── 0002_alter_favorite_unique_together_and_more.py
│   ├── templatetags/
│   │   └── dogs_tags.py
│   └── templates/dogs/
│       ├── base.html
│       ├── landing.html
│       ├── dashboard.html
│       ├── dog_list.html
│       ├── dog_detail.html
│       ├── dog_form.html
│       ├── profile.html
│       ├── login.html
│       ├── register.html
│       ├── matches.html
│       ├── favorites.html
│       ├── about.html
│       ├── contacts.html
│       ├── privacy.html
│       ├── tips.html
│       ├── events.html
│       ├── breeds.html
│       ├── error_404.html
│       ├── error_500.html
│       └── components/
│           ├── guest_menu.html
│           └── messages.html
├── menu_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── management/commands/
│   │   └── setup_menus.py
│   ├── migrations/
│   ├── templatetags/menu_tags.py
│   └── templates/menu/
│       ├── menu.html
│       └── menu_item.html
├── services/
│   ├── dog_service.py        # dog ownership & visibility checks
│   ├── favorites_service.py  # favorites toggle logic + permissions
│   └── match_service.py      # match creation/accept/decline logic
└── tests/
    ├── test_db.py
    ├── test_models.py
    ├── test_views.py
    ├── test_validations_and_services.py
    └── validate_guest_menu.py
```

---

## 🗃️ Database Models (Updated)

### Dog

- Basic profile (name, breed, age, gender, size, temperament, description)
- `owner = ForeignKey(User, related_name="dogs")`
- Age limited to 0–20 years (validator + form validation)
- Photo field with size and MIME type validation (JPEG, PNG, WebP)
- Unique constraint per owner: a user cannot create two dogs with the same name.
- `__str__` format: `"{name} ({owner.username})"`.

### Match

- Stores dog‑to‑dog matches with `status` (`pending`, `accepted`, `declined`).
- Unique constraint on `(dog_from, dog_to)` and indexes for efficient lookups.
- `__str__` includes both dog names and owners.

### Favorite

- Stores which dogs a user has favorited.
- `user = ForeignKey(User, related_name="favorite_dogs")`
- Unique constraint on `(user, dog)` + indexes on `user`, `dog`, and `(user, dog)`.

### UserProfile, Message, Menu

- Unchanged conceptually from the original README; provide extended user info, internal messaging, and navigation menu management.

---

## 🔌 API Endpoints (High Level)

This project is primarily server‑rendered HTML; the following are HTTP endpoints rather than a formal JSON API:

### Authentication

- `GET /register/`, `POST /register/` – user registration
- `GET /login/`, `POST /login/` – login
- `GET /logout/` – logout

### Dog Management

- `GET /dogs/` – list all dogs with filters + pagination
- `GET /dogs/<id>/` – dog detail view
- `GET/POST /dogs/create/` – create dog profile
- `GET/POST /dogs/<id>/edit/` – edit dog profile (owner‑only)
- `GET/POST /dogs/<id>/delete/` – delete dog profile (owner‑only)

### Matching & Favorites

- `GET /matches/` – list user’s matches with pagination
- `POST /dogs/<id>/favorite/` – toggle favorite via AJAX
- `GET /favorites/` – view favorites list with pagination

### User Management

- `GET /profile/` – profile view
- `GET/POST /profile/edit/` – edit profile
- `GET/POST /change-password/` – change password
- `GET/POST /delete-account/` – delete account

### Informational Pages

- `GET /about/`, `/contacts/`, `/privacy/`, `/tips/`, `/events/`, `/breeds/`, etc.

---

## 🧪 Testing

Run all tests:

```bash
python manage.py test
```

The suite includes:

- `test_db.py` – basic DB operations across apps
- `test_models.py` – model behavior (including `Dog.__str__`)
- `test_views.py` – form validation and basic view behavior
- `test_validations_and_services.py` –
  - Dog validators (age, per‑owner uniqueness)
  - Dog image validation via `DogForm`
  - Permissions in `dog_service`
  - Favorites and match flows via services
  - Pagination behavior (favorites) using Django’s `Paginator`
- `validate_guest_menu.py` – verifies guest menu integration in templates

All tests are currently passing under Django 4.2 in the configured venv.

---

## 🐳 Docker & Postgres

The repository includes a Docker setup for running the app with Postgres.

### Build & Run

```bash
docker compose up --build
```

This will start:

- `web` – Django app served by gunicorn using `project.settings.production`.
- `db` – Postgres 16 with database `dogdating`.

Environment in `docker-compose.yml`:

- `DJANGO_SETTINGS_MODULE=project.settings.production`
- `DATABASE_URL=postgres://dogdating_user:dogdating_password@db:5432/dogdating`

Data is stored in the `postgres_data` Docker volume.

---

## 🚀 Deployment

### Production Checklist

1. **Security settings**
   - `DEBUG = False` (use `production.py`)
   - Strong `SECRET_KEY` from `.env`
   - Correct `ALLOWED_HOSTS`
2. **Database**
   - Use Postgres with `DATABASE_URL`
   - Set up backups and monitoring
3. **Static files**
   - Run `python manage.py collectstatic`
   - Serve via a web server or CDN
4. **Media files**
   - Configure cloud storage (S3, MinIO, etc.) if needed
5. **Web server**
   - Use gunicorn/uvicorn behind Nginx or another reverse proxy
   - Configure HTTPS and HSTS

Production config is driven by `project.settings.production` and `.env` rather than the old single‑file example.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Add tests for new features.
5. Ensure all tests pass (`python manage.py test`).
6. Submit a pull request.

Coding guidelines:

- Follow PEP 8.
- Use meaningful commit messages.
- Add docstrings where appropriate.
- Use Russian for user‑facing content.

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support & FAQ

**Getting Help**

- Check the Django admin for debugging.
- Review logs in the console (structured logging enabled).
- Use Django’s built‑in debug tools in development.

**FAQ**

- **Q:** What language does the application use?
  - **A:** Russian (`LANGUAGE_CODE='ru-ru'`).
- **Q:** Can users have multiple dogs?
  - **A:** Yes, each user can create multiple dog profiles.
- **Q:** Is the site mobile‑friendly?
  - **A:** Yes, it uses responsive templates and mobile‑specific CSS.
- **Q:** How do I populate sample data?
  - **A:** Run `python manage.py setup_menus` and `python manage.py populate_data`.

---

Made with ❤️ for dog lovers everywhere. Woof! 🐕
