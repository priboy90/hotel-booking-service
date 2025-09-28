from datetime import date, timedelta

import pytest

from bookings.models import Booking
from bookings.services import BookingService
from rooms.models import Room


class TestBookingService:
    """Тесты для сервиса BookingService."""

    @pytest.mark.django_db
    def test_create_booking(self):
        """Тест создания брони через сервис."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)
        date_start = date.today()
        date_end = date.today() + timedelta(days=3)

        booking = BookingService.create_booking(room.id, date_start, date_end)

        assert booking.id is not None
        assert booking.room == room
        assert booking.date_start == date_start
        assert booking.date_end == date_end

        # Проверяем, что бронь сохранена в БД
        assert Booking.objects.filter(id=booking.id).exists()

    @pytest.mark.django_db
    def test_create_booking_nonexistent_room(self):
        """Тест создания брони для несуществующего номера."""
        with pytest.raises(Room.DoesNotExist):
            BookingService.create_booking(999, date.today(), date.today() + timedelta(days=2))

    @pytest.mark.django_db
    def test_delete_booking(self):
        """Тест удаления брони через сервис."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)
        booking = Booking.objects.create(room=room, date_start=date.today(), date_end=date.today() + timedelta(days=2))

        BookingService.delete_booking(booking.id)

        # Проверяем, что бронь удалена из БД
        assert not Booking.objects.filter(id=booking.id).exists()

    @pytest.mark.django_db
    def test_get_room_bookings(self):
        """Тест получения броней для номера."""
        room1 = Room.objects.create(description="Номер 1", price=2500.00)
        room2 = Room.objects.create(description="Номер 2", price=3500.00)

        # Создаем брони для разных номеров
        booking1 = Booking.objects.create(
            room=room1, date_start=date.today() + timedelta(days=5), date_end=date.today() + timedelta(days=7)
        )

        booking2 = Booking.objects.create(
            room=room1, date_start=date.today(), date_end=date.today() + timedelta(days=2)
        )

        Booking.objects.create(room=room2, date_start=date.today(), date_end=date.today() + timedelta(days=3))

        # Получаем брони только для room1
        bookings = BookingService.get_room_bookings(room1.id)

        assert len(bookings) == 2
        # Проверяем сортировку по дате начала
        assert bookings[0] == booking2  # Ранняя дата
        assert bookings[1] == booking1  # Поздняя дата

    @pytest.mark.django_db
    def test_get_room_bookings_empty(self):
        """Тест получения броней для номера без броней."""
        room = Room.objects.create(description="Номер без броней", price=2500.00)

        bookings = BookingService.get_room_bookings(room.id)

        assert len(bookings) == 0
