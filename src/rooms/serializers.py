# Импорт модуля сериализаторов из Django REST Framework
from rest_framework import serializers

# Импорт модели Room из текущего пакета (файл models.py в той же директории)
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Room (номер отеля)."""

    # Этот сериализатор используется для ЧТЕНИЯ и ОБНОВЛЕНИЯ данных о номере

    class Meta:
        # Указываем, какая модель будет сериализоваться
        model = Room

        # Перечисляем поля модели, которые будут включены в сериализацию
        # id - уникальный идентификатор номера
        # description - описание номера
        # price - цена номера
        # created_at - дата создания записи о номере
        fields = ["id", "description", "price", "created_at"]

        # Поля, которые доступны только для чтения
        # id и created_at генерируются автоматически и не могут быть изменены через API
        read_only_fields = ["id", "created_at"]


class RoomCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания номера (только необходимые поля)."""

    # Этот сериализатор используется только для СОЗДАНИЯ новых номеров
    # Он содержит минимальный набор полей, необходимых для создания

    class Meta:
        # Указываем, какая модель будет сериализоваться
        model = Room

        # Перечисляем только те поля, которые нужны при создании номера
        # description - описание номера (обязательное поле)
        # price - цена номера (обязательное поле)
        # Поля id и created_at не включаются, так как они генерируются автоматически
        fields = ["description", "price"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительной")
        return value
