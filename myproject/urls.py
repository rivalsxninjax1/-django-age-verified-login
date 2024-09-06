# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from myapp.views import signup  # Import the signup view from myapp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signup, name='signup'),  # Set the root URL to the signup page
    path('myapp/', include('myapp.urls')),  # Include URLs from myapp
]
