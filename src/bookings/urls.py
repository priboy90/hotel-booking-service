from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_booking, name="booking-create"),
    path("delete/<int:booking_id>/", views.delete_booking, name="booking-delete"),
    path("list/<int:room_id>/", views.list_room_bookings, name="booking-list"),
]
