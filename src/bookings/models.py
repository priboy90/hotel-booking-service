from django.db import models

from rooms.models import Room  # Импортируем модель Room


class Booking(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,  # Если номер удалят, все его брони тоже удалятся
        related_name="bookings",  # Позволит легко получить все брони номера: room.bookings.all()
        verbose_name="Номер",
    )
    date_start = models.DateField(verbose_name="Дата заезда")
    date_end = models.DateField(verbose_name="Дата выезда")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания брони")

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
        ordering = ["date_start"]  # Сортировка по умолчанию: по дате заезда

    def __str__(self):
        return f"Бронь #{self.id} (Номер #{self.room_id})"
