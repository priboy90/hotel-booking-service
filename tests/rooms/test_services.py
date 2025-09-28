import pytest

from rooms.models import Room
from rooms.services import RoomService


class TestRoomService:
    """Тесты для сервиса RoomService."""

    @pytest.mark.django_db
    def test_create_room(self):
        """Тест создания номера через сервис."""
        description = "Новый комфортабельный номер"
        price = 4000.00

        room = RoomService.create_room(description, price)

        assert room.id is not None
        assert room.description == description
        assert room.price == price

        # Проверяем, что номер действительно сохранен в БД
        assert Room.objects.filter(id=room.id).exists()

    @pytest.mark.django_db
    def test_delete_room(self):
        """Тест удаления номера через сервис."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)

        RoomService.delete_room(room.id)

        # Проверяем, что номер удален из БД
        assert not Room.objects.filter(id=room.id).exists()

    @pytest.mark.django_db
    def test_get_rooms_default_sorting(self):
        """Тест получения номеров с сортировкой по умолчанию."""
        room1 = Room.objects.create(description="Первый", price=1000.00)
        room2 = Room.objects.create(description="Второй", price=2000.00)

        rooms = RoomService.get_rooms()

        # По умолчанию сортировка по убыванию даты создания
        assert len(rooms) == 2
        assert rooms[0] == room2  # Новый номер первый
        assert rooms[1] == room1  # Старый номер второй

    @pytest.mark.django_db
    def test_get_rooms_sorted_by_price_asc(self):
        """Тест получения номеров с сортировкой по цене (по возрастанию)."""
        room1 = Room.objects.create(description="Дорогой", price=5000.00)
        room2 = Room.objects.create(description="Дешевый", price=1000.00)

        rooms = RoomService.get_rooms("price_asc")

        assert rooms[0] == room2  # Дешевый первый
        assert rooms[1] == room1  # Дорогой второй

    @pytest.mark.django_db
    def test_get_rooms_sorted_by_price_desc(self):
        """Тест получения номеров с сортировкой по цене (по убыванию)."""
        room1 = Room.objects.create(description="Дешевый", price=1000.00)
        room2 = Room.objects.create(description="Дорогой", price=5000.00)

        rooms = RoomService.get_rooms("price_desc")

        assert rooms[0] == room2  # Дорогой первый
        assert rooms[1] == room1  # Дешевый второй
