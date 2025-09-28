# wait_for_db.py
import os
import sys
import time

import django
from django.db import connections
from django.db.utils import OperationalError

# Добавляем src в путь Python ПЕРВЫМ элементом
src_path = os.path.join(os.path.dirname(__file__), "src")
sys.path.insert(0, src_path)  # ← ВАЖНО: insert(0, ...) а не append

# Настраиваем Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.config.settings")

django.setup()


def wait_for_db():
    """Ждем пока база данных будет готова"""
    max_retries = 30
    retry_delay = 2

    print("⏳ Waiting for database...")

    for i in range(max_retries):
        try:
            conn = connections["default"]
            conn.cursor()
            print("✅ Database is ready!")
            return True
        except OperationalError:
            if i < max_retries - 1:
                print(f"⏳ Waiting for database... ({i + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                print("❌ Database connection failed")
                return False


if __name__ == "__main__":
    success = wait_for_db()
    sys.exit(0 if success else 1)
