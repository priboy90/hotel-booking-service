import pytest
from django.urls import reverse
from rest_framework import status

from rooms.models import Room


class TestRoomViews:
    """Тесты для views приложения rooms."""

    @pytest.mark.django_db
    def test_create_room_success(self, client):
        """Тест успешного создания номера."""
        url = reverse("room-create")
        data = {"description": "Тестовый номер для создания", "price": 3500.00}

        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "room_id" in response.data
        assert Room.objects.filter(id=response.data["room_id"]).exists()

    @pytest.mark.django_db
    def test_create_room_invalid_data(self, client):
        """Тест создания номера с невалидными данными."""
        url = reverse("room-create")
        data = {
            "description": "",  # Пустое описание
            "price": -100.00,  # Отрицательная цена
        }

        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "description" in response.data
        assert "price" in response.data

    @pytest.mark.django_db
    def test_delete_room_success(self, client):
        """Тест успешного удаления номера."""
        room = Room.objects.create(description="Тестовый номер", price=2500.00)
        url = reverse("room-delete", args=[room.id])

        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Room.objects.filter(id=room.id).exists()

    @pytest.mark.django_db
    def test_delete_nonexistent_room(self, client):
        """Тест удаления несуществующего номера."""
        url = reverse("room-delete", args=[999])  # Несуществующий ID

        response = client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data

    @pytest.mark.django_db
    def test_list_rooms(self, client):
        """Тест получения списка номеров."""
        Room.objects.create(description="Первый номер", price=1000.00)
        Room.objects.create(description="Второй номер", price=2000.00)

        url = reverse("room-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_list_rooms_sorted(self, client):
        """Тест получения списка номеров с сортировкой."""
        Room.objects.create(description="Дорогой", price=5000.00)
        Room.objects.create(description="Дешевый", price=1000.00)

        url = reverse("room-list") + "?sort_by=price_asc"
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        # Проверяем сортировку по возрастанию цены
        assert response.data[0]["price"] == "1000.00"
        assert response.data[1]["price"] == "5000.00"
