"""
Разработать систему регистрации пользователя, используя Pydantic для валидации входных данных, обработки вложенных структур и сериализации.
Система должна обрабатывать данные в формате JSON.
Задачи:
    1. Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.
    2. Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic,
       валидирует данные, и в случае успеха сериализует объект обратно в JSON и возвращает его.
    3. Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости пользователя.
    4. Написать несколько примеров JSON строк для проверки различных сценариев валидации: успешные регистрации и случаи,
       когда валидация не проходит (например возраст не соответствует статусу занятости).
Модели:
Address: Должен содержать следующие поля:
    city: строка, минимум 2 символа.
    street: строка, минимум 3 символа.
    house_number: число, должно быть положительным.

User: Должен содержать следующие поля:
    name: строка, должна быть только из букв, минимум 2 символа.
    age: число, должно быть между 0 и 120.
    email: строка, должна соответствовать формату email.
    is_employed: булево значение, статус занятости пользователя.
    address: вложенная модель адреса.

Валидация:
Проверка, что если пользователь указывает, что он занят (is_employed = true), его возраст должен быть от 18 до 65 лет.
"""
from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError


class Address(BaseModel):
    city: str = Field(..., min_length=2, description="City's name.")
    street: str = Field(..., min_length=3, description="Street's name.")
    house_number: int = Field(gt=0, description="House number, positive integer.")


class User(BaseModel):
    name: str = Field(..., pattern=r'^[A-Za-z -]{2,50}$', description="User's name.")
    is_employed: bool = Field(True, description="User's is_employed.")
    age: int = Field(..., ge=0, le=120, description="User's age.")
    email: EmailStr = Field(..., description="User's email address.")
    address: Address

    # Проверка, что если пользователь указывает, что он занят (is_employed = true), его возраст должен быть от 18 до 65 лет.
    @field_validator('age')
    def validate_age(cls, value: int, values):
        is_employed = values.data.get('is_employed')
        if is_employed and not (18 <= value <= 65):
            raise TypeError(f"Age must be between 18 and 65")

        return value

def user_json_object(json_data):
    try:
        user = User.model_validate_json(json_data, strict=True) # проверяем на строгое соответствие типов (просто так)

        return user.model_dump_json(indent=2)

    except ValidationError as e:
        return e.json()


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
js_failed = (
    {"name": "Petr", "age": 16,"email": "petr@example.com", "is_employed": True,
     "address": {"city": "City city", "street": "Bbbbb bb", "house_number": 13}},
    {"name": "Maria", "age": 70, "email": "maria@example.com", "is_employed": True,
     "address": {"city": "city 333", "street": "street", "house_number": 5}},
    {"name": "John 123", "age": 63, "email": "john.doe@example.com", "is_employed": True,
     "address": {"city": "New York", "street": "5th Avenue", "house_number": 123}},
    {"name": "John", "age": 63, "email": "john.doe@example.com", "is_employed": True,
     "address": {"city": "New York", "street": "5th Avenue", "house_number": -13}},
    {"name": "John", "age": 63, "email": "john_example.com", "is_employed": True,
     "address": {"city": "New York", "street": "5th Avenue", "house_number": 13}},
)

import json

def check_user_json_object(jsons):
    for js in jsons:
        try:
            user = user_json_object(json.dumps(js))
            print(user)

        except ValidationError as e:
            print(e.json())

        except TypeError as e:
            print(e)

print(f"\n=== check OK ===")
check_user_json_object(js_ok)

print(f"\n=== check Failed ===")
check_user_json_object(js_failed)

