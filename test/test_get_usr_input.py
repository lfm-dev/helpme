import pytest
from usr_input.get_usr_input import is_int
#TODO tests with github actions

@pytest.mark.parametrize("input_test,expected", [
    ('0', True),
    ('10', True),
    ('-1', True),
    ('hola', False),
])
def test_is_int(input_test, expected):
    assert is_int(input_test) == expected