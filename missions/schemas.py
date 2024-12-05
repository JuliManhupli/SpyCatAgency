from typing import List

from ninja import Schema
from pydantic import field_validator

from cats.schemas import SpyCatSchema


class TargetSchema(Schema):
    id: int
    name: str
    country: str
    notes: str = ""
    is_completed: bool


class MissionSchema(Schema):
    id: int
    name: str
    description: str
    assigned_cat: SpyCatSchema | None
    is_completed: bool
    targets: List[TargetSchema]


class CreateTargetSchema(Schema):
    name: str
    country: str
    notes: str = ""

    @field_validator('name')
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError('Name must not be empty')
        return value

    @field_validator('country')
    def country_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError('Country must not be empty')
        return value

    @field_validator('notes')
    def notes_must_not_be_too_long(cls, value):
        if len(value) > 200:
            raise ValueError('Notes cannot exceed 200 characters')
        return value


class CreateMissionSchema(Schema):
    name: str
    description: str
    assigned_cat: int | None
    targets: List[CreateTargetSchema]

    @field_validator('name')
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError('Name must not be empty')
        return value

    @field_validator('description')
    def description_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError('Description must not be empty')
        return value
