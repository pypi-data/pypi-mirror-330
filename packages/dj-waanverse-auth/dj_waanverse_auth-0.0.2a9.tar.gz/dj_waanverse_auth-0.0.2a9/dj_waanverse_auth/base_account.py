"""
    Abstract base user model that supports both email and phone authentication.

    Includes core user management functionality and flexible contact methods."""

from typing import Optional

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models import Q
from django.utils import timezone


class AccountManager(BaseUserManager):
    def create_user(
        self,
        username: str,
        email_address: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields
    ):
        if not username:
            raise ValueError("Username is required")

        user = self.model(username=username, **extra_fields)
        if email_address:
            user.email_address = self.normalize_email(email_address)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username: str, email_address: str, password: str, **extra_fields
    ):
        if not email_address:
            raise ValueError("Superusers must have an email address")

        return self.create_user(
            username=username,
            email_address=email_address,
            password=password,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            **extra_fields
        )


class AbstractBaseAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=35,
        unique=True,
        db_index=True,
        help_text="Required. 10 characters or fewer.",
    )
    email_address = models.EmailField(
        max_length=255,
        verbose_name="Email",
        db_index=True,
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="E.164 format recommended (+1234567890)",
        db_index=True,
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password_last_updated = models.DateTimeField(default=timezone.now)
    email_verified = models.BooleanField(default=False)
    phone_number_verified = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email_address"]

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["phone_number"],
                name="%(app_label)s_%(class)s_unique_phone",
                condition=~Q(phone_number=None),
            ),
            models.UniqueConstraint(
                fields=["email_address"],
                name="%(app_label)s_%(class)s_unique_email",
                condition=~Q(email_address=None),
            ),
        ]
        indexes = [
            models.Index(
                fields=["username"], name="%(app_label)s_%(class)s_username_idx"
            ),
            models.Index(
                fields=["email_address"], name="%(app_label)s_%(class)s_email_idx"
            ),
            models.Index(
                fields=["phone_number"], name="%(app_label)s_%(class)s_phone_idx"
            ),
        ]

    def __str__(self) -> str:
        return self.get_primary_contact or self.username

    @property
    def get_primary_contact(self) -> Optional[str]:
        return self.email_address or self.phone_number or self.username

    def get_full_name(self) -> str:
        """
        Return the full name of the user, which is the username in this case.
        """
        return self.username

    def get_short_name(self) -> str:
        """
        Return the short name of the user, which is the username in this case.
        """
        return self.username

    def has_perm(self, perm: str, obj: Optional[object] = None) -> bool:
        """
        Check if the user has the specified permission. Only staff members have permissions.
        """
        return self.is_staff

    def has_module_perms(self, app_label: str) -> bool:
        """
        Check if the user has permission to access the given app label.
        """
        return True

    @property
    def can_receive_emails(self) -> bool:
        return self.email_address and self.email_verified
