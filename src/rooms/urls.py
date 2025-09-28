from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_room, name="room-create"),
    path("delete/<int:room_id>/", views.delete_room, name="room-delete"),
    path("list/", views.list_rooms, name="room-list"),
]
