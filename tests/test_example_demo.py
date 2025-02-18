## test case for demo
import pytest
import sys

# Define a marker in test module so that all tests in the module are run togther
pytestmark = pytest.mark.example_demo

# define a marker for specific test
@pytest.mark.smoke
def test_add_example():
    assert 2+3==5

# define a marker for specific test
@pytest.mark.smoke
def test_a1():
    print("This is my first test")
    assert 5 + 5 == 10
    assert 5 - 5 == 0
    assert 5 * 5 == 25
    assert 5 / 5 == 1

#assert statemnt failes raises exception as mentioned so test case will pass
@pytest.mark.smoke
@pytest.mark.exceptions
def test_case001():
    with pytest.raises(Exception) as exec_info:
        assert 2>5
    print(str(exec_info))