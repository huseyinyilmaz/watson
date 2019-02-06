"""Query managers for accounts app."""

import logging
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager
# from django.utils.text import slugify
# from core.utils import get_slug

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):

    """Query manager for accounts.User model."""

    use_in_migrations = True

    def _create_user_without_organization(self, email, password,
                                          is_staff, is_superuser,
                                          **extra_fields):
        """Create a User with the given username, email and password."""

        now = timezone.now()
        email = self.normalize_email(email)
        if not email:
            raise ValueError('The given email must be set')

        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """Create a User with the given username, email and password."""

        now = timezone.now()
        email = self.normalize_email(email)
        if not email:
            raise ValueError('The given email must be set')

        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now,
                          **extra_fields)
        user.set_password(password)
        organization = user.create_default_organization()
        user.default_organization = organization
        user.save(using=self._db)
        user.organizations.add(organization)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """Create a new user."""
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create a new superuser."""
        return self._create_user(email, password, True, True,
                                 **extra_fields)
