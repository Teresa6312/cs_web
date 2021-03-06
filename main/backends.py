from main.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class EmailBackend(object):
    def authenticate(self, username = None, password =None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except:
            return None

        if user.is_active and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None
