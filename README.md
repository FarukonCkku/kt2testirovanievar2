# Pytest: фикстуры и тестирование

Практические примеры тестирования с использованием **pytest** и фикстур.

## Содержание

1. [Метод, возвращающий длину строки](#1-метод-возвращающий-длину-строки)
2. [Метод, сохраняющий строку в файл](#2-метод-сохраняющий-строку-в-файл)
3. [Фикстура для подключения к SQLite](#3-фикстура-для-подключения-к-sqlite)
4. [Как запустить](#как-запустить)
5. [Полезные ссылки](#полезные-ссылки)

---

## 1. Метод, возвращающий длину строки

### Код

```python
# string_utils.py
def get_string_length(s: str) -> int:
    """Возвращает длину строки."""
    return len(s)
```

### Тесты

```python
# test_string_utils.py
from string_utils import get_string_length

def test_empty_string():
    assert get_string_length("") == 0

def test_multiline_string():
    text = "первая строка\nвторая строка\nтретья"
    assert get_string_length(text) == 33  # включая \n

def test_spaces_only():
    assert get_string_length("   ") == 3
    assert get_string_length("\t\n ") == 3

def test_normal_string():
    assert get_string_length("привет") == 6
```

**Покрытие:** пустая строка, многострочный текст, строка из пробелов/табуляций.

---

## 2. Метод, сохраняющий строку в файл

### Код

```python
# file_utils.py
def save_string_to_file(text: str, filepath: str) -> None:
    """Сохраняет строку в файл."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
```

### Тест с фикстурой `tmp_path`

```python
# test_file_utils.py
from file_utils import save_string_to_file

def test_save_string_to_file(tmp_path):
    # tmp_path — встроенная фикстура pytest
    file_path = tmp_path / "test.txt"
    content = "Привет, мир!\nВторая строка."

    save_string_to_file(content, str(file_path))

    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == content
```

Используется встроенная фикстура [`tmp_path`](https://docs.pytest.org/en/stable/how-to/tmp_path.html) — временная директория, которая автоматически очищается после теста.

---

## 3. Фикстура для подключения к SQLite

### Фикстура с очисткой (yield)

```python
# test_db.py
import pytest
import sqlite3

@pytest.fixture
def db_connection():
    """
    Создаёт in-memory SQLite соединение.
    После теста соединение закрывается.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    conn.commit()

    yield conn          # передаём соединение в тест

    conn.close()        # cleanup после теста
```

### Тесты

```python
def test_insert_and_select(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Алиса",))
    db_connection.commit()

    cursor.execute("SELECT name FROM users WHERE id = 1")
    result = cursor.fetchone()

    assert result is not None
    assert result[0] == "Алиса"


def test_empty_table(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    assert count == 0  # каждый тест получает чистую БД
```

Каждый тест получает **новое** in-memory соединение. После теста соединение закрывается.

---

## Как запустить

### Установка

```bash
pip install pytest
```

### Запуск всех тестов

```bash
pytest -v
```

### Запуск конкретного файла

```bash
pytest test_string_utils.py -v
pytest test_file_utils.py -v
pytest test_db.py -v
```

### С подробным выводом

```bash
pytest -v --tb=short
```

---

## Полезные ссылки

| Тема | Ссылка |
|------|--------|
| Фикстуры | [docs.pytest.org/en/stable/fixture.html](https://docs.pytest.org/en/stable/fixture.html) |
| `tmp_path` | [docs.pytest.org/en/stable/how-to/tmp_path.html](https://docs.pytest.org/en/stable/how-to/tmp_path.html) |
| Yield-фикстуры (setup/teardown) | [docs.pytest.org/en/stable/how-to/fixtures.html#yield-fixtures-recommended](https://docs.pytest.org/en/stable/how-to/fixtures.html#yield-fixtures-recommended) |
| Официальная документация pytest | [docs.pytest.org](https://docs.pytest.org) |

---

## Структура проекта (пример)

```
.
├── README.md
├── string_utils.py
├── file_utils.py
├── test_string_utils.py
├── test_file_utils.py
└── test_db.py
```

---

*Примеры подготовлены для обучения работе с pytest и фикстурами.*
