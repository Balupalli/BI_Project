import pytest

def pytest_configure():
    pytest.weekdays1=['MON','TUE','WED']
    pytest.weekdays2=['FRI','SAT','SUN']

@pytest.fixture(scope="module")
def setup003():
    wk1=pytest.weekdays1.copy()
    wk1.append('THURS')
    yield wk1

@pytest.fixture()
def setup004():
    wk2=pytest.weekdays2.copy()
    wk2.insert(0,'THURS')
    yield wk2


## fixture with request key word
@pytest.fixture()
def setup007(request):
    print(request.module.__name__)
    print(request.function.__name__)
    var= getattr(request.module, 'var_func')
    if var== 'SAI':
        yield var + str(' REDDY')
    else : yield var + str (' PRAKASH REDDY')

## fixture with request key word for factory of fixtures
@pytest.fixture()
def setup008():
    def get_db(db):
        if db=='MYSQL':
            yield str('MYSQL connection details')
        elif db=='SQL_SERVER':
            yield str('SQL-SERVER connection details')
        else: yield str('Snowflake connection details')
    yield get_db


