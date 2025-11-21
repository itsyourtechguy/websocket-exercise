from functions import add_numbers, multiply_numbers, echo
import pytest

def test_add_numbers():
    assert add_numbers(1, 2) == 3
    assert add_numbers(1.5, 2.5) == 4.0


def test_multiply_numbers():
    assert multiply_numbers(3, 4) == 12


def test_echo():
    assert echo("hello") == "hello"


def test_invalid_params():
    with pytest.raises(TypeError):
        add_numbers("x", "y")
