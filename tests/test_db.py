from menu_app.models import Menu, MenuItem
from dogs.models import Dog, UserProfile
from django.contrib.auth.models import User

# Test create
try:
    user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
    print('User created')
except:
    user = User.objects.get(username='testuser')
    print('User already exists')

menu = Menu.objects.create(name='test_menu', description='test menu description')
print('Menu created')
menu_item = MenuItem.objects.create(menu=menu, title='test menu item', url='/test')
print('MenuItem created')
dog = Dog.objects.create(owner=user, name='test_dog', breed='test_breed', age=1, gender='M', size='S', temperament='test_temperament', looking_for='playmate', description='test_description')
print('Dog created')
user_profile = UserProfile.objects.create(user=user, bio='test bio')
print('UserProfile created')


# Test read
print(Menu.objects.all())
print(MenuItem.objects.all())
print(Dog.objects.all())
print(UserProfile.objects.all())


# Test update
menu.description = 'updated description'
menu.save()
print('Menu updated')
dog.age = 2
dog.save()
print('Dog updated')

# Test delete
menu.delete()
print('Menu deleted')
dog.delete()
print('Dog deleted')
user_profile.delete()
print('UserProfile deleted')
user.delete()
print('User deleted')
