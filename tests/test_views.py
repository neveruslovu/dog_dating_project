import os
import sys
import django

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

# Import Django components after setup
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.auth.models import User
from dogs.views import landing_page, register, user_login, dashboard
from dogs.forms import UserRegistrationForm


def test_landing_page():
    print("Testing landing_page...")
    factory = RequestFactory()
    request = factory.get("/")

    # Add middleware
    middleware = SessionMiddleware(get_response=lambda r: r)
    middleware.process_request(request)
    request.session.save()

    try:
        response = landing_page(request)
        print(f"✓ Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_register_page():
    print("Testing register page...")
    factory = RequestFactory()
    request = factory.get("/register/")

    # Add middleware
    middleware = SessionMiddleware(get_response=lambda r: r)
    middleware.process_request(request)
    request.session.save()

    try:
        response = register(request)
        print(f"✓ Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_register_post():
    print("Testing register POST...")
    factory = RequestFactory()
    data = {
        "username": "testuser_view",
        "email": "test@example.com",
        "password1": "testpass123",
        "password2": "testpass123",
    }
    request = factory.post("/register/", data)

    # Add middleware
    middleware = SessionMiddleware(get_response=lambda r: r)
    middleware.process_request(request)
    request.session.save()

    # Add message middleware
    message_middleware = MessageMiddleware(get_response=lambda r: r)
    message_middleware.process_request(request)

    try:
        response = register(request)
        print(f"✓ Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_login_page():
    print("Testing login page...")
    factory = RequestFactory()
    request = factory.get("/login/")

    # Add middleware
    middleware = SessionMiddleware(get_response=lambda r: r)
    middleware.process_request(request)
    request.session.save()

    try:
        response = user_login(request)
        print(f"✓ Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_forms():
    print("Testing forms...")
    try:
        # Test UserRegistrationForm
        valid_data = {
            "username": "testform",
            "email": "testform@example.com",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        form = UserRegistrationForm(data=valid_data)
        if form.is_valid():
            print("✓ UserRegistrationForm valid")
        else:
            print(f"✗ UserRegistrationForm invalid: {form.errors}")
            return False
        return True
    except Exception as e:
        print(f"✗ Form error: {e}")
        return False


if __name__ == "__main__":
    print("=== Testing Views ===")
    results = []
    results.append(test_landing_page())
    print()
    results.append(test_register_page())
    print()
    results.append(test_register_post())
    print()
    results.append(test_login_page())
    print()
    results.append(test_forms())
    print()

    passed = sum(results)
    total = len(results)
    print(f"=== Results: {passed}/{total} tests passed ===")
