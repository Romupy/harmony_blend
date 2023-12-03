from django.urls import path
from . import views


urlpatterns = [
    path('create', views.create_profile, name="create_profile"),
    path('read/<profile_id>', views.read_profile, name="read_profile"),
    path('list', views.list_profiles, name="list_profiles"),
    path('update/<profile_id>', views.update_profile, name="update_profile"),
    path('delete/<profile_id>', views.delete_profile, name="delete_profile"),
]