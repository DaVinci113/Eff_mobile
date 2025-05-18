from django.urls import path, include
from .views import RegisterView


app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
]