# Импорт модуля сериализаторов из Django REST Framework
from rest_framework import serializers

from rooms.models import Room

# Импорт модели Room из указанного пути (приложение rooms в директории src)
# Импорт модели Booking из текущего пакета (файл models.py в той же директории)
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Booking (бронь)."""

    # Этот сериализатор используется для ЧТЕНИЯ и ОБНОВЛЕНИЯ данных о бронировании

    class Meta:
        # Указываем, какая модель будет сериализоваться - Booking
        model = Booking

        # Перечисляем поля модели, которые будут включены в сериализацию:
        # id - уникальный идентификатор брони
        # room - ссылка на номер отеля (внешний ключ к модели Room)
        # date_start - дата начала бронирования
        # date_end - дата окончания бронирования
        # created_at - дата и время создания записи о брони
        fields = ["id", "room", "date_start", "date_end", "created_at"]

        # Поля, которые доступны только для чтения:
        # id и created_at генерируются автоматически и не могут быть изменены через API
        read_only_fields = ["id", "created_at"]


class BookingCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания брони."""

    # Этот сериализатор используется только для СОЗДАНИЯ новых бронирований
    # Содержит пользовательскую валидацию для проверки корректности дат

    class Meta:
        # Указываем модель Booking для сериализации
        model = Booking

        # Перечисляем только те поля, которые нужны при создании брони:
        # room - номер для бронирования (обязательное поле)
        # date_start - дата начала брони (обязательное поле)
        # date_end - дата окончания брони (обязательное поле)
        fields = ["room", "date_start", "date_end"]

    def validate(self, data):
        """Валидация дат бронирования."""
        # data - словарь с проверяемыми данными (room, date_start, date_end)

        # Проверяем, что дата начала бронирования РАНЬШЕ даты окончания
        if data["date_start"] >= data["date_end"]:
            # Если дата начала >= даты окончания - выбрасываем ошибку валидации
            raise serializers.ValidationError("Дата окончания должна быть позже даты начала")

        # Если валидация прошла успешно - возвращаем данные
        return data

    def validate_room(self, room):
        """Проверяет, что номер существует."""
        # room уже будет объектом Room после первичной валидации
        if not Room.objects.filter(id=room.id).exists():
            raise serializers.ValidationError("Номер с указанным ID не существует")
        return room
