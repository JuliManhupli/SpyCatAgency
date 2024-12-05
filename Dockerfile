# Use an official Python runtime as the parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install Poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /code/

# Project initialization:
# Install all dependencies, including dev dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copying the rest of the application
COPY . /code/
