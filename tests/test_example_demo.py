## test case for demo
import pytest
import sys
import os

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

#parameterised test
@pytest.mark.parametrize('test_input',[10,20,30,40])
def test_param001(test_input):
    assert test_input%3 ==0

## define a fixture to build test data for function
@pytest.fixture()
def test_data():
    data=['SAI','PRAKASH','REDDY']
    return data

def test_name(test_data):
    assert len(test_data)==3

# write a fixture with yield
file='file1.txt'
@pytest.fixture()
def setup001():
    f= open(file,'w')
    f.write("py test example")
    f.close()
    f=open(file,'r+')
    yield f
    #tear down code
    f.close()
    os.remove(file) #delete file
def test_no4(setup001):
    assert (setup001.readline())=='py test example'

## fixture from conftest.py file used in function
@pytest.mark.fixtures_demo
def test_no5(setup003):
    del(setup003[-1])
    print(setup003)
    print(pytest.weekdays1)
    assert setup003==pytest.weekdays1 # we can used vairables defined in conftest.py directly
## undestand scope of fixtures
@pytest.mark.fixtures_demo
def test_no6(setup004):
    del(setup004[0])
    print(setup004)
    print(pytest.weekdays2)
    assert setup004== pytest.weekdays2

##example to check functionality of request
var_func='SAI'
def test_no7(setup007):
    assert setup007 =='SAI REDDY'

Database_used='MY_SQL'
# factory as fixtures
def test_no8(setup008):
    assert setup008('MYSQL')=='MYSQL connection details'