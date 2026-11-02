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
