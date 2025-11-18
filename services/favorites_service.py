from django.core.exceptions import PermissionDenied
from django.db import transaction

from dogs.models import Dog, Favorite


def toggle_favorite_for_user(user, dog_id: int) -> tuple[bool, str]:
    """Toggle favorite state for a dog on behalf of a specific user.

    Returns (is_favorite, message).
    Raises Dog.DoesNotExist if the dog does not exist or inactive.
    Raises PermissionDenied if the user is not allowed to perform the action.
    """
    if not user.is_authenticated:
        raise PermissionDenied("Требуется авторизация.")

    try:
        dog = Dog.objects.get(pk=dog_id, is_active=True)
    except Dog.DoesNotExist:
        # Let the caller decide how to render 404
        raise

    # We never trust a user id from the client: the caller passes request.user,
    # which prevents impersonation via forged user IDs.
    with transaction.atomic():
        favorite, created = Favorite.objects.get_or_create(user=user, dog=dog)
        if created:
            return True, f"{dog.name} добавлена в избранное"

        favorite.delete()
        return False, f"{dog.name} удалена из избранного"
