from django.urls import path
from . import views


urlpatterns = [
    path('register', views.register, name="register"),
    path('connection', views.connection, name="connection"),
    path('log_off', views.log_off, name="log_off"),
]
