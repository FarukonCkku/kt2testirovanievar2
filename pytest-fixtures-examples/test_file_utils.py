from file_utils import save_string_to_file


def test_save_string_to_file(tmp_path):
    # tmp_path — встроенная фикстура pytest
    file_path = tmp_path / "test.txt"
    content = "Привет, мир!\nВторая строка."

    save_string_to_file(content, str(file_path))

    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == content
