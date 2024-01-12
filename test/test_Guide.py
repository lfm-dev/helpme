import sys
import pytest
sys.path.append('../src')
from classes.Guide import Guide


@pytest.fixture
def my_guide():
    return Guide(
        filename = 'test_guide.md',
        path = '/here/is/the/guide',
        guides_path = 'here')

def test_get_filename_split(my_guide):
    assert my_guide.get_filename_split() == ['test', 'guide']

def test_get_partial_path_split(my_guide):
    assert my_guide.get_partial_path_split() == ['is', 'the', 'guide']

@pytest.mark.parametrize("input_test,expected", [
    (['test'], True),
    (['python'], False),
    (['test', 'guide'], True),
    (['test', 'the'], True),
    (['test', 'guide', 'javascript'], False)
])
def test_all_queries_in_keywords(my_guide, input_test, expected):
    assert my_guide.all_queries_in_keywords(input_test) == expected
