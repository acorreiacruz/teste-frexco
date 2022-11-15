from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameBackEnd(BaseBackend):
    def authenticate(
        self, request, username=None, password=None, authentication_field=None
    ):
        if not password:
            return None
        try:
            user = User.objects.get(
                Q(username=username or authentication_field)
                | Q(email=username or authentication_field)
            )
        except user.DoesNotExist:
            return None
        if self.user_can_authenticate(user) and user.check_password(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
        return user

    def user_can_authenticate(self, user):
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None