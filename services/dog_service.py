from django.core.exceptions import PermissionDenied

from dogs.models import Dog


def get_dog_for_owner(owner, dog_id, *, active_only: bool = True) -> Dog:
    """Return a dog owned by the given user or raise PermissionDenied.

    Centralizes the rule that only the owner may edit/delete a dog profile.
    """
    qs = Dog.objects.filter(pk=dog_id, owner=owner)
    if active_only:
        qs = qs.filter(is_active=True)
    try:
        return qs.get()
    except Dog.DoesNotExist:
        raise PermissionDenied("Нет доступа к этому профилю собаки.")


def get_public_dog(dog_id, *, active_only: bool = True) -> Dog:
    """Return a publicly viewable dog used for details/favorites/matches.

    Raises Dog.DoesNotExist if the dog is not found (or inactive when active_only=True).
    """
    qs = Dog.objects.all()
    if active_only:
        qs = qs.filter(is_active=True)
    return qs.get(pk=dog_id)
