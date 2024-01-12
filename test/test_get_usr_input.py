import sys
import pytest
sys.path.append('../src')
from usr_input.get_usr_input import is_int

@pytest.mark.parametrize("input_test,expected", [
    ('0', True),
    ('10', True),
    ('-1', True),
    ('hola', False),
])
def test_thing_with_input(input_test, expected):
    assert is_int(input_test) == expected