def save_string_to_file(text: str, filepath: str) -> None:
    """Сохраняет строку в файл."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
