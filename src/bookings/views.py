# Импорт необходимых модулей из Django REST Framework
from rest_framework import status  # HTTP статусы (200, 201, 404, etc.)
from rest_framework.decorators import api_view  # Декоратор для создания API view
from rest_framework.response import Response  # Класс для формирования HTTP ответов

from rooms.models import Room

from .models import Booking

# Импорт сериализаторов из текущего пакета
from .serializers import BookingCreateSerializer, BookingSerializer

# Импорт сервисного слоя для бизнес-логики бронирований
from .services import BookingService


@api_view(["POST"])  # Разрешаем только POST запросы к этой функции
def create_booking(request):
    """Создание новой брони."""

    # Создаем сериализатор с данными из запроса
    serializer = BookingCreateSerializer(data=request.data)

    # Проверяем валидность данных (вызывает метод validate() из сериализатора)
    if serializer.is_valid():
        try:
            # Если данные валидны, создаем бронирование через сервисный слой
            booking = BookingService.create_booking(
                room_id=serializer.validated_data["room"].id,  # Извлекаем ID комнаты из объекта
                date_start=serializer.validated_data["date_start"],
                date_end=serializer.validated_data["date_end"],
            )
            # Возвращаем успешный ответ с ID созданной брони
            return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Обрабатываем ошибки бизнес-логики из сервиса
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Если данные не прошли валидацию сериализатора
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_booking(request, booking_id):
    try:
        # Сначала проверяем существование брони
        Booking.objects.get(id=booking_id)
        BookingService.delete_booking(booking_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Booking.DoesNotExist:
        return Response({"error": "Бронь не найдена"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])  # Разрешаем только GET запросы
def list_room_bookings(request, room_id):
    """Получение списка броней для номера."""
    try:
        # Сначала проверяем существование комнаты
        Room.objects.get(id=room_id)

        # Получаем список бронирований для конкретной комнаты через сервис
        bookings = BookingService.get_room_bookings(room_id)

        # Сериализуем данные (many=True для списка объектов)
        serializer = BookingSerializer(bookings, many=True)

        # Возвращаем сериализованные данные
        return Response(serializer.data)

    except Room.DoesNotExist:
        return Response({"error": "Комната не найдена"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
