import requests
from ninja import Schema
from pydantic import field_validator


def validate_breed(breed: str) -> bool:
    response = requests.get('https://api.thecatapi.com/v1/breeds')
    breeds = [b['name'].title() for b in response.json()]
    return breed.title() in breeds


class SpyCatSchema(Schema):
    id: int
    name: str
    years_of_experience: int
    breed: str
    salary: float


class UpdateSalarySchema(Schema):
    salary: float

    @field_validator('salary')
    def salary_must_be_positive(cls, value):
        if value < 0:
            raise ValueError('Salary must be a positive number')
        return value

class CreateSpyCatSchema(Schema):
    name: str
    years_of_experience: int
    breed: str
    salary: float

    @field_validator('name')
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError('Name must not be empty')
        return value

    @field_validator('years_of_experience')
    def years_of_experience_must_be_positive(cls, value):
        if value < 0:
            raise ValueError('Years of experience must be a positive number')
        return value

    @field_validator('breed')
    def breed_must_be_valid(cls, value):
        if not validate_breed(value):
            raise ValueError(f"{value} is not a valid breed")
        return value

    @field_validator('salary')
    def salary_must_be_positive(cls, value):
        if value < 0:
            raise ValueError('Salary must be a positive number')
        return value
