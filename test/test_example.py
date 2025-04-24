import pytest

def test_equal_or_not():
    assert 1 == 1

def test_is_instance():
    assert isinstance("test", str)
    assert not isinstance("10", int)

def test_boolean():
    validated = True
    assert validated is True

def test_type():
    assert type("Hello") is str

def test_greater_or_less():
    assert 7 > 1
    assert 5 < 10

def test_list():
    num_list = [1, 2, 3]
    assert 1 in num_list

class Student():

    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_student():
    return Student("John", "Doe", "science", 20)


def test_person_initialization(default_student):
    assert isinstance(default_student.first_name, str)
    assert isinstance(default_student.last_name, str)
    assert isinstance(default_student.major, str)
    assert isinstance(default_student.years, int)
    assert default_student.first_name == "John"
    assert default_student.last_name == "Doe"
    assert default_student.years > 18, "Student is too young"
