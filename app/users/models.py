from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

# from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=("first name"))
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=("last name"))
    is_staff = models.BooleanField(
        verbose_name=("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this site."),
    )
    is_active = models.BooleanField(
        verbose_name=("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
