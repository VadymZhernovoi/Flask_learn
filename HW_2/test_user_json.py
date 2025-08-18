import pytest
from pydantic import ValidationError, ValidationInfo
import json
from hw_2 import user_json_object

js_ok = (
    {"name": "John Doe", "age": 65, "email": "john.doe@example.com", "is_employed": True,
     "address": { "city": "New York", "street": "5th Avenue", "house_number": 123}},
    {"name": "Ivan Ivanov", "age": 18, "email": "ivan@example.com", "is_employed": True,
     "address": {"city": "City 1", "street": "Street 1", "house_number": 1}},
    {"name": "Anna", "age": 16, "email": "anna@example.com", "is_employed": False,
     "address": {"city": "City 2", "street": "Street 2", "house_number": 2}},
    {"name": "Vd", "age": 0, "email": "vd@ex.cc", "is_employed": False,
     "address": {"city": "12", "street": "Ddqwd wfwf wff wffr fbcb 2122121", "house_number": 999}}
)
expected_ok = (
    ["John Doe", 65, "john.doe@example.com", True, "New York", "5th Avenue", 123],
    ["Ivan Ivanov", 18, "ivan@example.com", True, "City 1", "Street 1", 1],
    ["Anna", 16, "anna@example.com", False, "City 2", "Street 2", 2],
    ["Vd", 0, "vd@ex.cc", False, "12", "Ddqwd wfwf wff wffr fbcb 2122121", 999]
)

@pytest.mark.parametrize(
    "js, expected",
    [
        (js_ok[0], expected_ok[0]),
        (js_ok[1], expected_ok[1]),
        (js_ok[2], expected_ok[2]),
        (js_ok[3], expected_ok[3]),
    ]
)
def test_ok_returns_json(js, expected):
    out = user_json_object(json.dumps(js))
    data = json.loads(out)
    assert data["name"] == expected[0]
    assert data["age"] == expected[1]
    assert data["email"] == expected[2]
    assert data["is_employed"] == expected[3]
    assert data["address"]["city"] == expected[4]
    assert data["address"]["street"] == expected[5]
    assert data["address"]["house_number"] == expected[6]

@pytest.mark.parametrize("age", [16, 66])  # вне диапазона 18–65
def test_name_invalid(age):
    bad = {
        "name": "John Ddddd",
        "age": age,
        "email": "john.doe@example.com",
        "is_employed": True,
        "address": {"city": "New York", "street": "5th Avenue", "house_number": 333},
    }
    with pytest.raises(ValidationError):
        user_json_object(json.dumps(bad, ensure_ascii=False))

js_bad = (
    {"name": "John 123", "age": 63, "email": "john.doe@example.com", "is_employed": True,
     "address": {"city": "New York", "street": "5th Avenue", "house_number": 123}},
    {"name": "John", "age": 63, "email": "john.doe@example.com", "is_employed": True,
     "address": {"city": "New York", "street": "5th Avenue", "house_number": -13}},
    {"name": "John", "age": 63, "email": "john_example.com", "is_employed": True,
     "address": {"city": "New York", "street": "5th Avenue", "house_number": 13}},
)
@pytest.mark.parametrize(
    "js",
    [
        js_bad[0],
        js_bad[1],
        js_bad[2],
    ]
)
def test_user_invalid_fields(js):
     with pytest.raises(ValidationError):
        user_json_object(json.dumps(js))
