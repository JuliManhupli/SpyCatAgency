from django.shortcuts import get_object_or_404

from .models import SpyCat
from .schemas import CreateSpyCatSchema


def create_spy_cat(payload: CreateSpyCatSchema) -> SpyCat:
    try:
        spy_cat = SpyCat.objects.create(**payload.dict())
        return spy_cat
    except Exception as e:
        raise Exception(f"Failed to create spy cat: {str(e)}")


def list_spy_cats() -> list:
    try:
        return list(SpyCat.objects.all())
    except Exception as e:
        raise Exception(f"Failed to list spy cats: {str(e)}")


def get_spy_cat(cat_id: int) -> SpyCat:
    """Get spy cat by ID or raise 404."""
    return get_object_or_404(SpyCat, id=cat_id)


def update_spy_cat(cat_id: int, payload: CreateSpyCatSchema) -> SpyCat:
    try:
        spy_cat = get_spy_cat(cat_id)
        for attr, value in payload.dict().items():
            setattr(spy_cat, attr, value)
        spy_cat.save()
        return spy_cat
    except Exception as e:
        raise Exception(f"Failed to update spy cat: {str(e)}")


def update_spy_cat_salary(cat_id: int, new_salary: float) -> SpyCat:
    try:
        spy_cat = get_spy_cat(cat_id)
        spy_cat.salary = new_salary
        spy_cat.save()
        return spy_cat
    except Exception as e:
        raise Exception(f"Failed to update salary for cat with ID {cat_id}: {str(e)}")


def delete_spy_cat(cat_id: int) -> None:
    try:
        spy_cat = get_spy_cat(cat_id)
        spy_cat.delete()
    except Exception as e:
        raise Exception(f"Failed to delete spy cat: {str(e)}")