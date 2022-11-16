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


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-id",)
        db_table = "users"

    first_name = models.CharField(max_length=150, blank=True, null=False)
    last_name = models.CharField(max_length=150, blank=True, null=False)
    username = models.CharField(max_length=150, blank=False, null=False, unique=True)
    email = models.CharField(max_length=150, blank=False, null=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    birth_date = models.DateField(blank=False, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    def __str__(self):
        return self.username