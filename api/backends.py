from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from abc import abstractmethod, ABC


User = get_user_model()


class CustomBackEnd(BaseBackend, ABC):
    @abstractmethod
    def authenticate(self, request, authentication_field=None, password=None , username=None):
        pass
    
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
        return user

    def user_can_authenticate(self, user):
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None


class EmailBackEnd(CustomBackEnd):
    def authenticate(self, request, authentication_field=None, password=None , username=None):
        if not password:
            return None
        try:
            user = User.objects.get(email=username or authentication_field)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None


class UsernameBackEnd(CustomBackEnd):
    def authenticate(self, request, authentication_field=None, password=None , username=None):
        if not password:
            return None
        try:
            user = User.objects.get(username=username or authentication_field)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
