from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path('login/', auth_login, name='login'),
    path('logout/', logout_view, name='logout'),
]