from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import paginate, PageNumberPagination

from .schemas import SpyCatSchema, CreateSpyCatSchema, UpdateSalarySchema
from .services import (
    create_spy_cat,
    list_spy_cats,
    get_spy_cat,
    update_spy_cat,
    update_spy_cat_salary,
    delete_spy_cat,
)

router = Router(tags=["Cats"])


@router.post("/", response=SpyCatSchema)
def create_spy_cat_view(request, payload: CreateSpyCatSchema):
    try:
        spy_cat = create_spy_cat(payload)
        return spy_cat
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")


@router.get("/", response=list[SpyCatSchema])
@paginate(PageNumberPagination, page_size=5)
def list_spy_cats_view(request):
    try:
        return list_spy_cats()
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")


@router.get("/{cat_id}/", response=SpyCatSchema)
def get_spy_cat_view(request, cat_id: int):
    try:
        return get_spy_cat(cat_id)
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")


@router.put("/{cat_id}/", response=SpyCatSchema)
def update_spy_cat_view(request, cat_id: int, payload: CreateSpyCatSchema):
    try:
        return update_spy_cat(cat_id, payload)
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")


@router.patch("/{cat_id}/salary", response=SpyCatSchema)
def update_salary_view(request, cat_id: int, data: UpdateSalarySchema):
    try:
        return  update_spy_cat_salary(cat_id, data.salary)
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")


@router.delete("/{cat_id}/", response=dict)
def delete_spy_cat_view(request, cat_id: int):
    try:
        delete_spy_cat(cat_id)
        return {"success": True}
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")
