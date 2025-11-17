# DogDating - Django Dog Dating Platform
<img width="2559" height="1334" alt="image" src="https://github.com/user-attachments/assets/4ac3d399-539c-4ab4-8181-d9a2f306a625" />
<img width="2555" height="1333" alt="image" src="https://github.com/user-attachments/assets/b0e514d7-3b66-4b81-bfe8-6114ff7aecce" />



![DogDating Logo](https://img.shields.io/badge/DogDating-🐕-blue?style=for-the-badge)
![Django Version](https://img.shields.io/badge/Django-4.2+-green?style=flat-square)
![Python Version](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

DogDating is a modern web application built with Django that helps dog owners find compatible companions for their pets. The platform features advanced matching algorithms, user profiles, messaging system, and a beautiful responsive design.

## 🌟 Features

### Core Functionality

- **User Authentication System** - Registration, login, password management
- **Dog Profile Management** - Create, edit, and manage multiple dog profiles
- **Advanced Matching Algorithm** - AI-powered compatibility scoring based on breed, age, size, temperament, and preferences
- **Favorites System** - Save dogs you're interested in
- **Match Management** - Send, receive, accept, or decline match requests
- **Messaging System** - Communicate with other dog owners
- **Search & Filters** - Advanced search with multiple filters (breed, age, size, gender)
- **Pagination** - Efficient handling of large datasets

### Technical Features

- **Responsive Design** - Mobile-first, works perfectly on all devices
- **Image Upload & Optimization** - Automatic image optimization and default placeholders
- **AJAX Interactions** - Smooth, asynchronous user experience
- **Error Handling** - Custom 404 and 500 error pages
- **Admin Panel** - Comprehensive Django admin interface
- **Database Optimization** - Efficient queries with select_related and prefetch_related

### UI/UX Features

- **Modern Design** - Beautiful gradient backgrounds and card-based layouts
- **Loading States** - Loading spinners and toast notifications
- **Interactive Elements** - Hover effects and smooth transitions
- **Accessibility** - Proper semantic HTML and ARIA labels

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

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

# Email configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Media Files

The application uses Django's media files for image uploads. Images are automatically optimized and stored in:

- Dog photos: `media/dogs/`
- User avatars: `media/avatars/`

### Database Configuration

The project uses SQLite by default. For production, consider PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dogdating',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

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
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── DATABASE_TUTORIAL.md      # Database documentation
├── project/                  # Project configuration
│   ├── __init__.py
│   ├── settings.py           # Django settings
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
│   ├── migrations/          # Database migrations
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
│           ├── error_404.html
│           └── error_500.html
└── menu_app/                 # Menu management app
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    ├── templates/
    │   └── menu/
    └── templatetags/
        └── menu_tags.py
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
- Status tracking (pending, accepted, declined)
- Timestamp tracking

#### Message

- User-to-user messaging
- Subject and content
- Read/unread status

#### Favorite

- User's favorite dogs
- Many-to-many relationship
- Timestamp tracking

### Model Relationships

```
User ←→ UserProfile (1:1)
User ←→ Dog (1:many)
Dog ←→ Match (1:many, two relationships)
User ←→ Message (1:many, two relationships)
User ←→ Favorite (1:many)
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

- `POST /matches/<id>/favorite/` - Toggle favorite
- `GET /matches/` - List user's matches
- `POST /matches/<id>/accept/` - Accept match
- `POST /matches/<id>/decline/` - Decline match

### User Management

- `GET /profile/` - User profile view
- `PUT /profile/edit/` - Update profile
- `POST /password/change/` - Change password
- `POST /account/delete/` - Delete account

### AJAX Endpoints

- `POST /toggle-favorite/<id>/` - AJAX favorite toggle
- All standard endpoints support AJAX where appropriate

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

- User authentication
- Dog CRUD operations
- Matching algorithm
- Forms validation
- AJAX interactions

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

- [Database Tutorial](DATABASE_TUTORIAL.md) - Detailed database guide
- [API Documentation](docs/api.md) - Complete API reference
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Deployment Guide](docs/deployment.md) - Production deployment

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
- Use Black for code formatting
- Write meaningful commit messages
- Add docstrings to functions and classes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help

- 📧 Email: <support@dogdating.com>
- 🐛 Bug Reports: [GitHub Issues](https://github.com/yourusername/dog-dating/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/dog-dating/discussions)

### FAQ

**Q: How does the matching algorithm work?**
A: The algorithm calculates compatibility based on age difference, size compatibility, gender preferences, matching goals, breed similarity, and temperament keywords.

**Q: Can users have multiple dogs?**
A: Yes, each user can create profiles for multiple dogs.

**Q: Is the site mobile-friendly?**
A: Yes, the entire application is built with a mobile-first responsive design.

**Q: How are images optimized?**
A: Images are automatically resized and compressed when uploaded, with default placeholders for missing images.

## 🎯 Roadmap

### Upcoming Features

- [ ] Mobile app (React Native)
- [ ] Advanced filtering (location-based, distance)
- [ ] Video chat integration
- [ ] Event planning features
- [ ] Veterinary service integration
- [ ] Social media sharing
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

### Version History

- **v1.0.0** - Initial release with core features
- **v1.1.0** - Image optimization and error pages
- **v1.2.0** - Enhanced matching algorithm
- **v1.3.0** - Mobile optimization

---

Made with ❤️ for dog lovers everywhere. Woof! 🐕
