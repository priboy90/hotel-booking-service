from datetime import date, timedelta

import pytest

from bookings.models import Booking
from rooms.models import Room


class TestBookingModel:
    """Тесты для модели Booking."""

    @pytest.mark.django_db
    def test_create_booking(self):
        """Тест создания брони."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)

        booking = Booking.objects.create(room=room, date_start=date.today(), date_end=date.today() + timedelta(days=3))

        assert booking.id is not None
        assert booking.room == room
        assert booking.date_start == date.today()
        assert booking.date_end == date.today() + timedelta(days=3)
        assert booking.created_at is not None

    @pytest.mark.django_db
    def test_booking_string_representation(self):
        """Тест строкового представления брони."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)
        booking = Booking.objects.create(room=room, date_start=date.today(), date_end=date.today() + timedelta(days=2))

        expected_str = f"Бронь #{booking.id} (Номер #{room.id})"
        assert str(booking) == expected_str

    @pytest.mark.django_db
    def test_booking_ordering(self):
        """Тест сортировки броней."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)

        booking1 = Booking.objects.create(
            room=room, date_start=date.today() + timedelta(days=5), date_end=date.today() + timedelta(days=7)
        )

        booking2 = Booking.objects.create(room=room, date_start=date.today(), date_end=date.today() + timedelta(days=2))

        bookings = Booking.objects.all()

        # Должны быть отсортированы по дате начала (по возрастанию)
        assert bookings[0] == booking2  # Ранняя дата начала
        assert bookings[1] == booking1  # Поздняя дата начала
