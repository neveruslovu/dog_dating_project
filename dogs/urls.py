from django.urls import path
from . import views

app_name = 'dogs'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_dog, name='register'),
    path('profile/<int:dog_id>/', views.dog_profile, name='profile'),
    path('matches/', views.matches, name='matches'),
    path('about/', views.about, name='about'),
    path('breeds/', views.breeds, name='breeds'),
    path('events/', views.events, name='events'),
    path('tips/', views.tips, name='tips'),
]