import pytest
from django.test import Client


@pytest.fixture
def client():
    """Фикстура для тестового клиента."""
    return Client()
