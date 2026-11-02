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
