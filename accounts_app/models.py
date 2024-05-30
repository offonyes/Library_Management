from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

from accounts_app.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(
        max_length=100, null=False, blank=False, verbose_name=_("First Name")
    )
    last_name = models.CharField(
        max_length=100, null=False, blank=False, verbose_name=_("Last Name")
    )
    personal_number = models.CharField(
        max_length=11, null=False, blank=False, verbose_name=_("Personal Number"), validators=[MinLengthValidator(11)]
    )
    birth_date = models.DateField(
        null=False, blank=False, verbose_name=_("Date of Birth")
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='customuser_groups',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='customuser_user_permissions',
        related_query_name='user',
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "personal_number", "birth_date"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
