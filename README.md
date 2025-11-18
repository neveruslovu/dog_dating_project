# DogDating - Django Dog Dating Platform

![DogDating Logo](https://img.shields.io/badge/DogDating-🐕-blue?style=for-the-badge)
![Django Version](https://img.shields.io/badge/Django-4.2+-green?style=flat-square)
![Python Version](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
<img width="2539" height="1245" alt="image" src="https://github.com/user-attachments/assets/b3c7b64b-8ba9-4d0e-8145-a129abd5523a" />
<img width="2541" height="1274" alt="image" src="https://github.com/user-attachments/assets/a69504af-f6ff-431c-a3b7-d7904b506213" />
<img width="1123" height="635" alt="image" src="https://github.com/user-attachments/assets/0e84afb2-057b-4750-bc6d-86e253f43e79" />
<img width="2536" height="895" alt="image" src="https://github.com/user-attachments/assets/4e987062-84a9-4fff-9696-0d22f7dbb8dd" />

DogDating is a modern web application built with Django that helps dog owners find compatible companions for their pets. The platform features user profiles, matching system, favorites, and a responsive design with Russian language support.

## 🌟 Features

### Core Functionality

- **User Authentication System** - Registration, login, password management
- **Dog Profile Management** - Create, edit, and manage multiple dog profiles
- **Matching System** - Basic compatibility matching between dogs
- **Favorites System** - Save dogs you're interested in
- **Match Management** - View and manage match requests
- **User Profiles** - Extended user information with avatars
- **Search & Browse** - View all dogs with basic filtering
- **Dashboard** - Central hub for user activities
- **Guest Menu System** - Navigation for non-authenticated users ✨ **NEW**

### Additional Features

- **Multi-language Support** - Russian language interface (LANGUAGE_CODE: ru-ru)
- **Menu Management System** - Dynamic menu via menu_app
- **Custom Error Pages** - 404 and 500 error handling
- **Template Components** - Reusable template components
- **Image Optimization** - Automatic image resizing and optimization for uploads
- **Management Commands** - Data population and menu setup commands

### Technical Features

- **Django 4.2+** - Modern Django framework with latest features
- **SQLite Database** - Lightweight database for development and small deployments
- **Template System** - Django templates with custom template tags
- **Static Files Management** - Organized static and media file handling
- **Error Handling** - Custom 404 and 500 error pages
- **Admin Panel** - Django admin interface for content management
- **Management Commands** - Custom Django management commands for data setup

### UI/UX Features

- **Responsive Design** - Mobile-first design with full mobile support ✨ **NEW**
- **Mobile Optimized** - Tested on iPhone, Android, tablets ✨ **NEW**
- **Russian Language** - Full Russian language interface
- **Component-based Templates** - Reusable template components
- **Clean Layout** - Simple, user-friendly design
- **Navigation System** - Dynamic menu management
- **Touch-Friendly** - Optimized for touch screens and gestures ✨ **NEW**
- **Notch Support** - Works with iPhone X+ and Android notches ✨ **NEW**
- **Dark/Light Theme** - Automatic theme switching based on OS preferences

## 📱 Mobile Support

This project is **fully optimized for mobile devices**! Features include:

- ✅ Responsive grid system (320px - 1920px+)
- ✅ Touch-friendly interface (48x48px minimum touch targets)
- ✅ iPhone X+ notch support with safe area insets
- ✅ Android device support (Samsung, Google Pixel, etc.)
- ✅ Tablet support (iPad, Samsung Galaxy Tab)
- ✅ Landscape/Portrait orientation handling
- ✅ Fast performance on 4G/3G networks
- ✅ Optimized images with lazy loading

**See [MOBILE_OPTIMIZATION.md](./MOBILE_OPTIMIZATION.md) for detailed mobile features!**

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/dog-dating.git
   cd dog-dating
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Note: The project uses Django>=4.2,<5.0 as the main dependency.

4. **Database setup**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: <http://127.0.0.1:8000>
   - Admin panel: <http://127.0.0.1:8000/admin>

8. **Optional: Populate sample data**

   ```bash
   python manage.py populate_data
   ```

## ⚙️ Configuration

### Environment Variables

The project uses environment variables for configuration. Key settings:

- `SECRET_KEY` - Auto-generated if not provided
- `DEBUG` - Set to True for development
- `ALLOWED_HOSTS` - Defaults to ["localhost", "127.0.0.1"]
- `LANGUAGE_CODE` - Set to "ru-ru" (Russian)
- `TIME_ZONE` - Set to "Europe/Moscow"

### Media Files

The application uses Django's media files for image uploads. Images are automatically optimized and stored in:

- Dog photos: `media/dogs/`
- User avatars: `media/avatars/`

### Database Configuration

The project uses SQLite by default with `db.sqlite3` file. The current configuration includes:

- SQLite database for development
- Basic user authentication models
- Dog profiles and matching system
- Menu management system

For production, consider PostgreSQL or MySQL for better performance.

## 📖 Usage

### Getting Started

1. **Register an Account**
   - Visit the landing page
   - Click "Registration"
   - Fill in your details

2. **Create Your Dog Profile**
   - Go to "Add Dog" from the dashboard
   - Upload a photo and fill in details
   - Set preferences for what you're looking for

3. **Browse and Match**
   - View the list of all dogs
   - Use filters to find compatible dogs
   - Send match requests to dogs you like

4. **Manage Matches**
   - View your pending matches
   - Accept or decline match requests
   - Chat with matched dogs' owners

### User Roles

#### Regular Users

- Create and manage dog profiles
- Browse other dogs
- Send and receive match requests
- Send messages to matched users
- Manage favorites

#### Administrators

- Access to Django admin panel
- Manage all users, dogs, and content
- View site statistics
- Moderate content

## 📁 Project Structure

```
dog_dating_project/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies (Django>=4.2,<5.0)
├── README.md                 # This file
├── db.sqlite3               # SQLite database file
├── project/                  # Project configuration
│   ├── __init__.py
│   ├── settings.py           # Django settings (Russian locale)
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── dogs/                     # Main application
│   ├── __init__.py
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py              # App configuration
│   ├── forms.py             # Django forms
│   ├── models.py            # Database models
│   ├── urls.py              # App URL patterns
│   ├── utils.py             # Utility functions
│   ├── views.py             # View functions
│   ├── views_new.py         # Additional views
│   ├── management/          # Management commands
│   │   └── commands/
│   │       └── populate_data.py  # Data population command
│   ├── migrations/          # Database migrations
│   ├── templatetags/        # Custom template tags
│   │   └── dogs_tags.py
│   └── templates/           # HTML templates
│       └── dogs/
│           ├── base.html
│           ├── landing.html
│           ├── dashboard.html
│           ├── dog_list.html
│           ├── dog_detail.html
│           ├── dog_form.html
│           ├── profile.html
│           ├── login.html
│           ├── register.html
│           ├── matches.html
│           ├── favorites.html
│           ├── about.html
│           ├── contacts.html
│           ├── privacy.html
│           ├── tips.html
│           ├── events.html
│           ├── breeds.html
│           ├── error_404.html
│           ├── error_500.html
│           └── components/
│               └── guest_menu.html
│               └── messages.html
├── menu_app/                 # Menu management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── management/          # Management commands
│   │   └── commands/
│   │       └── setup_menus.py  # Menu setup command
│   ├── migrations/
│   ├── templatetags/
│   │   └── menu_tags.py
│   └── templates/
│       └── menu/
│           ├── menu.html
│           └── menu_item.html
└── tests/                    # Test suite
    ├── test_db.py
    ├── test_models.py
    ├── test_views.py
    └── validate_guest_menu.py # Guest menu implementation test
```

## 🗃️ Database Models

### Core Models

#### User (Django Built-in)

- Basic authentication and user management
- Extended with OneToOne UserProfile

#### Dog

- Dog profile information
- Owner relationship
- Matching preferences
- Photo uploads

#### UserProfile

- Extended user information
- Bio, location, phone
- Avatar uploads

#### Match

- Dog-to-dog matching system
- Status tracking
- Timestamp tracking

#### Favorite

- User's favorite dogs
- Many-to-many relationship
- Timestamp tracking

#### Menu (menu_app)

- Dynamic menu management
- Hierarchical menu structure
- Multi-language support

### Model Relationships

```
User ←→ UserProfile (1:1)
User ←→ Dog (1:many)
Dog ←→ Match (1:many)
User ←→ Favorite (1:many)
Menu ←→ MenuItem (1:many)
```

## 🔌 API Endpoints

### Authentication

- `POST /register/` - User registration
- `POST /login/` - User login
- `POST /logout/` - User logout

### Dog Management

- `GET /dogs/` - List all dogs with filters
- `GET /dogs/<id>/` - Dog detail view
- `POST /dogs/create/` - Create new dog profile
- `PUT /dogs/<id>/edit/` - Update dog profile
- `DELETE /dogs/<id>/delete/` - Delete dog profile

### Matching System

- `GET /matches/` - List user's matches
- `POST /matches/<id>/favorite/` - Toggle favorite

### User Management

- `GET /profile/` - User profile view
- `POST /profile/edit/` - Update profile
- `POST /password/change/` - Change password
- `POST /account/delete/` - Delete account

### Additional Pages

- `GET /about/` - About page
- `GET /contacts/` - Contact information
- `GET /privacy/` - Privacy policy
- `GET /tips/` - Dog care tips
- `GET /events/` - Events page
- `GET /breeds/` - Dog breeds information

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test dogs

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Coverage

The project includes tests for:

- Database operations (`test_db.py`)
- Model functionality (`test_models.py`)
- View functionality (`test_views.py`)
- Guest menu implementation (`validate_guest_menu.py`)

## 🚀 Deployment

### Production Checklist

1. **Security Settings**
   - Set `DEBUG = False`
   - Use strong `SECRET_KEY`
   - Configure `ALLOWED_HOSTS`

2. **Database**
   - Use PostgreSQL or MySQL
   - Set up database backups
   - Configure connection pooling

3. **Static Files**

   ```bash
   python manage.py collectstatic
   ```

4. **Media Files**
   - Configure cloud storage (AWS S3, Google Cloud, etc.)
   - Set up CDN for images

5. **Web Server**
   - Use Gunicorn or uWSGI
   - Configure Nginx as reverse proxy
   - Set up SSL certificates

### Example Production Settings

```python
# production.py
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dogdating',
        'USER': 'dogdating_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static and Media files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_STORAGE_BUCKET_NAME = 'dogdating-media'
AWS_S3_REGION_NAME = 'us-east-1'
```

## 📚 Documentation

- **[README.md](README.md)** - Project overview and setup guide
- **[MOBILE_OPTIMIZATION.md](MOBILE_OPTIMIZATION.md)** - Comprehensive mobile adaptation guide ✨ **NEW**
- **[MOBILE_TESTING_GUIDE.md](MOBILE_TESTING_GUIDE.md)** - How to test mobile features ✨ **NEW**
- **Inline code documentation** - Docstrings in models, views, and utilities
- **Django Admin** - Built-in admin interface for data management

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Write meaningful commit messages
- Add docstrings to functions and classes
- Use Russian language for user-facing content

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help

- 📧 Check the Django admin panel for debugging
- 🐛 Review the error logs in the console
- 💬 Use Django's built-in debugging tools in development mode

### FAQ

**Q: What language does the application use?**
A: The application interface is in Russian (LANGUAGE_CODE: ru-ru).

**Q: Can users have multiple dogs?**
A: Yes, each user can create profiles for multiple dogs.

**Q: Is the site mobile-friendly?**
A: Yes, the application uses responsive design templates.

**Q: How do I populate sample data?**
A: Use the management command `python manage.py populate_data`.

**Q: How do I set up the menu system?**
A: Use the management command `python manage.py setup_menus`.

## 🎯 Roadmap

### Current Features

- ✅ User authentication and registration
- ✅ Dog profile management
- ✅ Basic matching system
- ✅ Favorites functionality
- ✅ Russian language interface
- ✅ Menu management system
- ✅ Custom error pages
- ✅ Management commands for data setup

### Potential Future Enhancements

- [ ] Advanced matching algorithms
- [ ] Location-based search
- [ ] Mobile app development
- [ ] Multi-language support beyond Russian
- [ ] Social features and events
- [ ] Advanced messaging system

---

Made with ❤️ for dog lovers everywhere. Woof! 🐕

**Current Status**: Development project with Django 4.2+, Russian language support, and basic dog dating functionality.
