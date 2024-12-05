from django.shortcuts import get_object_or_404
from cats.models import SpyCat
from .models import Mission, Target
from .schemas import CreateMissionSchema


def get_mission_or_404(mission_id: int) -> Mission:
    """Gets a mission or raises a 404 error if not found."""
    return get_object_or_404(Mission, id=mission_id)


def get_target_or_404(target_id: int) -> Target:
    """Gets a target or raises a 404 error if not found."""
    return get_object_or_404(Target, id=target_id)


def check_if_cat_not_assigned(mission: Mission) -> None:
    """Checks if there is an not assigned cat to the mission."""
    if not mission.assigned_cat:
        raise ValueError("Cannot modify mission without an assigned cat.")


def check_if_completed(target: Target) -> None:
    """Checks if the target or mission is completed."""
    if target.is_completed or target.mission.is_completed:
        raise ValueError("Cannot modify completed target or mission.")


def create_mission_with_targets(payload: CreateMissionSchema) -> Mission:
    try:
        assigned_cat = SpyCat.objects.get(id=payload.assigned_cat) if payload.assigned_cat else None

        # Create mission
        mission = Mission.objects.create(
            name=payload.name,
            description=payload.description,
            assigned_cat=assigned_cat,
            is_completed=False,
        )

        # Create associated targets
        for target in payload.targets:
            Target.objects.create(
                mission=mission,
                name=target.name,
                country=target.country,
                notes=target.notes,
                is_completed=False
            )

        return mission
    except SpyCat.DoesNotExist:
        raise ValueError(f"Spy cat with ID {payload.assigned_cat} not found.")
    except Exception as e:
        raise Exception(f"Failed to create mission: {str(e)}")


def list_missions() -> list:
    try:
        return list(Mission.objects.all())
    except Exception as e:
        raise Exception(f"Failed to list missions: {str(e)}")


def get_mission(cat_id: int) -> Mission:
    return get_mission_or_404(cat_id)


def assign_cat_to_mission(mission_id: int, cat_id: int) -> Mission:
    try:
        mission = get_mission_or_404(mission_id)
        cat = SpyCat.objects.get(id=cat_id)

        if mission.is_completed:
            raise ValueError("Cannot assign a cat to a completed mission.")

        mission.assigned_cat = cat
        mission.save()
        return mission
    except SpyCat.DoesNotExist:
        raise Exception(f"Spy cat with ID {cat_id} not found.")
    except Exception as e:
        raise Exception(f"Failed to assign cat to mission: {str(e)}")


def remove_cat_from_mission(mission_id: int) -> Mission:
    try:
        mission = get_mission_or_404(mission_id)

        if mission.is_completed:
            raise ValueError("Cannot remove a cat from a completed mission.")

        mission.assigned_cat = None
        mission.save()
        return mission
    except Exception as e:
        raise Exception(f"Failed to remove cat from mission: {str(e)}")


def delete_mission(mission_id: int) -> None:
    try:
        mission = get_mission_or_404(mission_id)

        if mission.assigned_cat:
            raise ValueError("Cannot delete mission assigned to a cat.")

        mission.delete()
    except Exception as e:
        raise Exception(f"Failed to delete mission: {str(e)}")


def update_target_notes(target_id: int, new_notes: str):
    try:
        target = get_target_or_404(target_id)

        check_if_cat_not_assigned(target.mission)
        check_if_completed(target)

        target.notes = new_notes
        target.save()

        return target
    except Exception as e:
        raise Exception(f"Failed to update target notes: {str(e)}")


def mark_target_as_completed(target_id: int):
    try:
        target = get_target_or_404(target_id)

        check_if_cat_not_assigned(target.mission)

        target.is_completed = True
        target.save()

        if all(t.is_completed for t in target.mission.targets.all()):
            target.mission.is_completed = True
            target.mission.save()

        return target
    except Exception as e:
        raise Exception(f"Failed to mark target as completed: {str(e)}")
