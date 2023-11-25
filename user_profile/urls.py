from django.urls import path
from . import views


urlpatterns = [
    path('create', views.create, name="profile_create"),
    path('<profile_id>', views.read, name="profile_read"),
]