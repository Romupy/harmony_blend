from django.urls import path
from . import views


urlpatterns = [
    path(
        'read/<user_profile_id>',
        views.read_user_profile,
        name="read_user_profile"
    ),
    path('list', views.list_user_profiles, name="list_user_profiles"),
    path(
        'update',
        views.update_user_profile,
        name="update_user_profile"
    ),
]
