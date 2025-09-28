import pytest

from rooms.models import Room


class TestRoomModel:
    """Тесты для модели Room."""

    @pytest.mark.django_db
    def test_create_room(self):
        """Тест создания номера."""
        room = Room.objects.create(description="Комфортабельный номер с видом на море", price=3500.00)

        assert room.id is not None
        assert room.description == "Комфортабельный номер с видом на море"
        assert room.price == 3500.00
        assert room.created_at is not None

    @pytest.mark.django_db
    def test_room_string_representation(self):
        """Тест строкового представления номера."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)

        assert str(room) == f"Номер #{room.id} - 2500.00 руб./ночь"

    @pytest.mark.django_db
    def test_room_ordering(self):
        """Тест сортировки номеров."""
        room1 = Room.objects.create(description="Первый номер", price=1000.00)
        room2 = Room.objects.create(description="Второй номер", price=2000.00)

        rooms = Room.objects.all()

        # Должны быть отсортированы по убыванию даты создания (новые сверху)
        assert rooms[0] == room2
        assert rooms[1] == room1
