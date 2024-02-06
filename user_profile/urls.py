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
        'update/<user_profile_id>',
        views.update_user_profile,
        name="update_user_profile"
    ),
    path(
        'delete/<user_profile_id>',
        views.delete_user_profile,
        name="delete_user_profile"
    ),
]
