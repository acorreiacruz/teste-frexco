from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def __field_error(self, field, message):
        if not field:
            raise ValueError(message)

    def create_user(self, username, email, password, **other_fields):
        self.__field_error(username,"A user must have a username !")
        self.__field_error(email,"A user must have a email address")
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        user = self.create_user(username, email, password, **other_fields)
        user.save()
        return user
