# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('verify-age/', views.verify_age, name='verify_age'),
    path('request-verification/', views.request_verification, name='request_verification'),
    path('manage-verification-requests/', views.manage_verification_requests, name='manage_verification_requests'),
    path('waiting-for-verification/', views.waiting_for_verification, name='waiting_for_verification'),
    path('login-successful/', views.login_successful, name='login_successful'),
]
