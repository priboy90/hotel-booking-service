from .models import Room


class RoomService:
    """Сервис для работы с номерами отеля."""

    @staticmethod
    def create_room(description: str, price: float) -> Room:
        """Создание нового номера отеля."""
        room = Room.objects.create(description=description, price=price)
        return room

    @staticmethod
    def delete_room(room_id: int) -> None:
        """Удаление номера отеля и всех его броней."""
        Room.objects.filter(id=room_id).delete()

    @staticmethod
    def get_rooms(sort_by: str | None = None) -> list[Room]:
        """Получение списка номеров с возможностью сортировки."""
        rooms = Room.objects.all()

        if sort_by == "price_asc":
            rooms = rooms.order_by("price")
        elif sort_by == "price_desc":
            rooms = rooms.order_by("-price")
        elif sort_by == "date_asc":
            rooms = rooms.order_by("created_at")
        elif sort_by == "date_desc":
            rooms = rooms.order_by("-created_at")

        return list(rooms)
