from datetime import date, timedelta

import pytest

from bookings.serializers import BookingCreateSerializer
from rooms.models import Room


class TestBookingSerializer:
    """Тесты для сериализаторов Booking."""

    @pytest.mark.django_db
    def test_booking_create_serializer_valid(self):
        """Тест валидных данных для создания брони."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)

        data = {
            "room": room.id,
            "date_start": date.today().isoformat(),
            "date_end": (date.today() + timedelta(days=3)).isoformat(),
        }

        serializer = BookingCreateSerializer(data=data)
        assert serializer.is_valid()

    @pytest.mark.django_db
    def test_booking_create_serializer_invalid_dates(self):
        """Тест невалидных дат для брони."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)

        data = {
            "room": room.id,
            "date_start": (date.today() + timedelta(days=3)).isoformat(),  # Дата начала позже окончания
            "date_end": date.today().isoformat(),
        }

        serializer = BookingCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    @pytest.mark.django_db
    def test_booking_create_serializer_same_dates(self):
        """Тест одинаковых дат начала и окончания."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)

        today = date.today().isoformat()
        data = {
            "room": room.id,
            "date_start": today,
            "date_end": today,  # Та же дата
        }

        serializer = BookingCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    @pytest.mark.django_db
    def test_booking_serializer_read_only_fields(self):
        """Тест полей только для чтения."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)

        data = {
            "id": 999,  # Поле только для чтения
            "created_at": "2023-01-01T00:00:00Z",  # Поле только для чтения
            "room": room.id,
            "date_start": date.today().isoformat(),
            "date_end": (date.today() + timedelta(days=2)).isoformat(),
        }

        serializer = BookingCreateSerializer(data=data)
        # Поля только для чтения должны игнорироваться при создании
        assert serializer.is_valid()
