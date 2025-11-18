from django.core.exceptions import PermissionDenied
from django.db import transaction

from dogs.models import Dog, Match
from dogs.utils import create_match, accept_match, decline_match


def create_match_for_user(user, dog_from_id: int, dog_to_id: int) -> Match:
    """Create a match initiated by the given user.

    Ensures the source dog belongs to the user, both dogs exist, and the
    target dog is not owned by the same user.
    """
    try:
        dog_from = Dog.objects.get(pk=dog_from_id, owner=user, is_active=True)
    except Dog.DoesNotExist:
        raise PermissionDenied("Нет доступа к исходной собаке.")

    try:
        dog_to = Dog.objects.get(pk=dog_to_id, is_active=True)
    except Dog.DoesNotExist:
        # propagate for the view to render 404
        raise

    if dog_to.owner == user:
        raise PermissionDenied("Нельзя создавать мэтч со своей собакой.")

    with transaction.atomic():
        return create_match(dog_from, dog_to)


def accept_match_for_user(user, match: Match) -> bool:
    """Accept a match if the user owns one of the dogs involved."""
    if match.dog_to.owner != user and match.dog_from.owner != user:
        raise PermissionDenied("Нет доступа к этому мэтчу.")
    return accept_match(match)


def decline_match_for_user(user, match: Match) -> bool:
    """Decline a match if the user owns one of the dogs involved."""
    if match.dog_to.owner != user and match.dog_from.owner != user:
        raise PermissionDenied("Нет доступа к этому мэтчу.")
    return decline_match(match)
