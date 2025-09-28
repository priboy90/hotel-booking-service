from rooms.serializers import RoomCreateSerializer


class TestRoomSerializer:
    """Тесты для сериализаторов Room."""

    def test_room_serializer(self):
        """Тест сериализатора RoomSerializer."""
        data = {"description": "Тестовый номер", "price": "3000.00"}

        serializer = RoomCreateSerializer(data=data)
        assert serializer.is_valid()

        validated_data = serializer.validated_data
        assert validated_data["description"] == "Тестовый номер"
        assert validated_data["price"] == 3000.00

    def test_room_serializer_invalid_data(self):
        """Тест сериализатора с невалидными данными."""
        data = {
            "description": "",  # Пустое описание
            "price": "-100.00",  # Отрицательная цена
        }

        serializer = RoomCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "description" in serializer.errors
        assert "price" in serializer.errors

    def test_room_serializer_missing_fields(self):
        """Тест сериализатора с отсутствующими полями."""
        data = {}  # Пустые данные

        serializer = RoomCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "description" in serializer.errors
        assert "price" in serializer.errors
