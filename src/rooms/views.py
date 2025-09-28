# Импорт необходимых модулей из Django REST Framework
from rest_framework import status  # Импорт HTTP статусов (200, 201, 404 и т.д.)
from rest_framework.decorators import api_view  # Декоратор для создания API view
from rest_framework.response import Response  # Класс для создания HTTP ответов

from .models import Room

# Импорт сериализаторов из текущего пакета (файл serializers.py)
from .serializers import RoomCreateSerializer, RoomSerializer

# Импорт сервисного слоя для работы с бизнес-логикой комнат
from .services import RoomService


@api_view(["POST"])  # Декоратор: разрешаем только POST запросы к этой функции
def create_room(request):
    """Создание нового номера отеля."""

    # Создаем сериализатор с данными из запроса
    serializer = RoomCreateSerializer(data=request.data)

    # Проверяем валидность данных (вызывает метод validate() сериализатора)
    if serializer.is_valid():
        # Если данные валидны, создаем комнату через сервисный слой
        room = RoomService.create_room(
            description=serializer.validated_data["description"],  # Безопасные данные после валидации
            price=serializer.validated_data["price"],
        )
        # Возвращаем успешный ответ с ID созданной комнаты и статусом 201 Created
        return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)

    # Если данные невалидны, возвращаем ошибки валидации со статусом 400 Bad Request
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_room(request, room_id):
    try:
        # Сначала проверяем существование комнаты
        Room.objects.get(id=room_id)
        RoomService.delete_room(room_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Room.DoesNotExist:
        return Response({"error": "Комната не найдена"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])  # Декоратор: разрешаем только GET запросы
def list_rooms(request):
    """Получение списка номеров с сортировкой."""

    # Получаем параметр сортировки из query string (?sort_by=price)
    sort_by = request.GET.get("sort_by")

    # Получаем отсортированный список комнат через сервисный слой
    rooms = RoomService.get_rooms(sort_by)

    # Сериализуем данные (many=True - сериализуем список объектов)
    serializer = RoomSerializer(rooms, many=True)

    # Возвращаем сериализованные данные со статусом 200 OK
    return Response(serializer.data)
