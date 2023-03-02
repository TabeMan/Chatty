from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('<slug:profile_slug>/', views.ProfileView.as_view(), name='profile'),
    path('<slug:profile_slug>/update/', views.EditProfileView.as_view(), name='edit_profile'),
]
