from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import paginate, PageNumberPagination

from .schemas import MissionSchema, CreateMissionSchema, TargetSchema
from .services import (
    create_mission_with_targets,
    list_missions,
    get_mission,
    assign_cat_to_mission,
    remove_cat_from_mission,
    delete_mission,
    mark_target_as_completed,
    update_target_notes,

)

router = Router(tags=["Missions"])


@router.post("/", response=MissionSchema)
def create_mission_view(request, payload: CreateMissionSchema):
    try:
        create_mission = create_mission_with_targets(payload)
        return create_mission
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")


@router.get("/", response=list[MissionSchema])
@paginate(PageNumberPagination, page_size=5)
def list_missions_view(request):
    try:
        return list_missions()
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")


@router.get("/{mission_id}/", response=MissionSchema)
def get_mission_view(request, mission_id: int):
    try:
        return get_mission(mission_id)
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")


@router.patch("/{mission_id}/assign-cat/{cat_id}/", response=MissionSchema)
def assign_cat_to_mission_view(request, mission_id: int, cat_id: int):
    try:
        return assign_cat_to_mission(mission_id, cat_id)
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")


@router.patch("/{mission_id}/remove-cat/", response=MissionSchema)
def remove_cat_from_mission_view(request, mission_id: int):
    try:
        return remove_cat_from_mission(mission_id)
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")


@router.patch("/{mission_id}/target/{target_id}/complete/", response=TargetSchema)
def mark_target_as_completed_view(request, mission_id: int, target_id: int):
    try:
        return mark_target_as_completed(target_id)
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")


@router.patch("/{mission_id}/target/{target_id}/notes/", response=TargetSchema)
def update_target_notes_view(request, mission_id: int, target_id: int, new_notes: str):
    try:
        return update_target_notes(target_id, new_notes)
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")


@router.delete("/{mission_id}/", response=dict)
def delete_mission_view(request, mission_id: int):
    try:
        delete_mission(mission_id)
        return {"success": True}
    except Exception as e:
        raise HttpError(400, f"Error: {str(e)}")