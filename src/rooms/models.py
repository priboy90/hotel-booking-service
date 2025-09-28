from django.db import models


class Room(models.Model):
    description = models.TextField(verbose_name="Описание номера")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за ночь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ["-created_at"]  # Сортировка по умолчанию: новые сверху

    def __str__(self):
        return f"Номер #{self.id} - {self.price:.2f} руб./ночь"
