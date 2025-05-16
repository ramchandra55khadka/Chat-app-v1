from django.urls import path
from .views import HomeView, RoomView, SignOutView

urlpatterns = [
    path("", HomeView, name="login"),
    path("<str:room_name>/", RoomView, name="room"),
    path("logout/", SignOutView, name="logout"),
]
