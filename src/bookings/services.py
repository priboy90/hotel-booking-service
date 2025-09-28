from rooms.models import Room

from .models import Booking


class BookingService:
    """Сервис для работы с бронированиями."""

    @staticmethod
    def create_booking(room_id: int, date_start: str, date_end: str) -> Booking:
        """Создание новой брони."""
        # Проверяем, существует ли номер
        room = Room.objects.get(id=room_id)

        overlapping_bookings = Booking.objects.filter(room=room, date_start__lt=date_end, date_end__gt=date_start)
        if overlapping_bookings.exists():
            raise Exception("Номер уже забронирован на указанные даты")

        # Создаем бронь
        booking = Booking.objects.create(room=room, date_start=date_start, date_end=date_end)
        return booking

    @staticmethod
    def delete_booking(booking_id: int) -> None:
        """Удаление брони."""
        Booking.objects.filter(id=booking_id).delete()

    @staticmethod
    def get_room_bookings(room_id: int) -> list[Booking]:
        """Получение списка броней для конкретного номера."""
        bookings = Booking.objects.filter(room_id=room_id).order_by("date_start")
        return list(bookings)
