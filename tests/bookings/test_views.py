from datetime import date, timedelta

import pytest
from django.urls import reverse
from rest_framework import status

from bookings.models import Booking
from rooms.models import Room


class TestBookingViews:
    """Тесты для views приложения bookings."""

    @pytest.mark.django_db
    def test_create_booking_success(self, client):
        """Тест успешного создания брони."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)

        url = reverse("booking-create")
        data = {
            "room": room.id,
            "date_start": date.today().isoformat(),
            "date_end": (date.today() + timedelta(days=3)).isoformat(),
        }

        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "booking_id" in response.data
        assert Booking.objects.filter(id=response.data["booking_id"]).exists()

    @pytest.mark.django_db
    def test_create_booking_invalid_dates(self, client):
        """Тест создания брони с невалидными датами."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)

        url = reverse("booking-create")
        data = {
            "room": room.id,
            "date_start": (date.today() + timedelta(days=3)).isoformat(),  # Дата начала позже окончания
            "date_end": date.today().isoformat(),
        }

        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data or "non_field_errors" in response.data

    @pytest.mark.django_db
    def test_create_booking_nonexistent_room(self, client):
        """Тест создания брони для несуществующего номера."""
        url = reverse("booking-create")
        data = {
            "room": 999,  # Несуществующий номер
            "date_start": date.today().isoformat(),
            "date_end": (date.today() + timedelta(days=2)).isoformat(),
        }

        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # Проверяем наличие ошибки в поле room
        assert "room" in response.data

    @pytest.mark.django_db
    def test_delete_booking_success(self, client):
        """Тест успешного удаления брони."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)
        booking = Booking.objects.create(room=room, date_start=date.today(), date_end=date.today() + timedelta(days=2))

        url = reverse("booking-delete", args=[booking.id])
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Booking.objects.filter(id=booking.id).exists()

    @pytest.mark.django_db
    def test_delete_nonexistent_booking(self, client):
        """Тест удаления несуществующей брони."""
        url = reverse("booking-delete", args=[999])
        response = client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data

    @pytest.mark.django_db
    def test_list_room_bookings(self, client):
        """Тест получения списка броней для номера."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)

        # Создаем несколько броней
        Booking.objects.create(room=room, date_start=date.today(), date_end=date.today() + timedelta(days=2))

        Booking.objects.create(
            room=room, date_start=date.today() + timedelta(days=5), date_end=date.today() + timedelta(days=7)
        )

        url = reverse("booking-list", args=[room.id])
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_list_room_bookings_empty(self, client):
        """Тест получения списка броней для номера без броней."""
        room = Room.objects.create(description="Номер без броней", price=2500.00)

        url = reverse("booking-list", args=[room.id])
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    @pytest.mark.django_db
    def test_list_room_bookings_nonexistent_room(self, client):
        """Тест получения броней для несуществующего номера."""
        url = reverse("booking-list", args=[999])
        response = client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data
