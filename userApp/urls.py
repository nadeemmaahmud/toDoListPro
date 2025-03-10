from django.urls import path
from . views import user_profile, user_logout, user_login, user_register, change_password, reset_password_request, reset_password_confirm, verify_email, contact, about

urlpatterns = [
    path('', user_profile, name='user_profile'),
    path('logout/', user_logout, name='user_logout'),
    path('login/', user_login, name='user_login'),
    path('register/', user_register, name='user_register'),
    path("verify-email/<uidb64>/<token>/", verify_email, name="verify_email"),
    path('change_password/', change_password, name='change_password'),
    path("reset-password/", reset_password_request, name="reset_password_request"),
    path("reset-password/<uidb64>/<token>/", reset_password_confirm, name="reset_password_confirm"),
    path("contact/", contact, name="contact"),
    path("about/", about, name="about"),
]