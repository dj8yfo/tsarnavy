from django.contrib.contenttypes.models import ContentType
from .models import Action

LOGIN = "logged in "
POST_CREATE = "created"
POST_LIKE = "liked"
POST_UNLIKE = "unliked"

def create_action(user, verb, target=None):
    action = Action(user=user, verb=verb, target=target)
    action.save()
    return True
