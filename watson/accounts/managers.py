"""Query managers for accounts app."""

import logging
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils.text import slugify
from uuid import uuid4

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):

    """Query manager for accounts.User model."""

    use_in_migrations = True

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """Create a User with the given username, email and password."""

        now = timezone.now()
        email = self.normalize_email(email)
        if not email:
            raise ValueError('The given email must be set')
        registration_code = uuid4().hex

        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now,
                          registration_code=registration_code,
                          **extra_fields)
        user.set_password(password)
        user.create_organization()
        user.save(using=self._db)
        user.organizations.add(user.default_organization)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """Create a new user."""
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create a new superuser."""
        return self._create_user(email, password, True, True,
                                 **extra_fields)


def get_slug(model, user, postfix=None):
    # Add a prefix to slug to make sure uniqness.
    if postfix is None:
        postfix_str = ''
    else:
        postfix_str = str(postfix)
    slug = f'${slugify(user.name)}${postfix_str}'

    if model.objects.filter(slug=slug).exists():
        if postfix is None:
            postfix = 1
        else:
            postfix = postfix + 1
        return get_slug(model, user, postfix)
    else:
        return slug

class OrganizationManager(models.Manager):

    def create_for_user(self, user):
        slug = get_slug(self.model, user)
        # user might not be on db yet.(id might be None)
        # XXX slug should be unique
        obj = self.model.objects.create(email=user.email,
                                        name=user.email,
                                        slug=slug)
        return obj
