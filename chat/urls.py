from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('chat/create/', views.CreateRoomView.as_view(), name='create_room'),
    path('chat/<slug:room_slug>/', views.RoomView.as_view(), name='room'),
]
