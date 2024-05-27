from django.contrib.auth.views import LoginView
from django.urls import path
from users.apps import UsersConfig
from users.views import logout_view, RegisterView, ProfileView, generate_new_password, confirm_registration, \
    invalid_token_view, reset_password

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-registration/<str:token>/', confirm_registration, name='confirm_registration'),
    path('invalid-token/', invalid_token_view, name='invalid_token'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/genpassword', generate_new_password, name='generate_new_password'),
    path('reset_password/', reset_password, name='reset_password'),
]