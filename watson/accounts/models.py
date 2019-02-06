import logging
from django.db import models

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.core.mail import send_mail
from django.utils import timezone as tz

from django_extensions.db.models import TimeStampedModel

from core.utils import get_slug
from accounts import managers
import uuid

logger = logging.getLogger(__name__)


class Organization(TimeStampedModel):

    """Organization Model."""

    # mandatory fields
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255)
    # optional field
    company = models.CharField(max_length=1024, blank=True)
    location = models.CharField(max_length=2048, blank=True)
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        is_created = not self.pk
        result = super().save(*args, **kwargs)
        if is_created:
            # creat default project for organization.
            Project.objects.create(
                organization=self,
                name='Default Project',
                slug='default',
                default=True,
            )
        return result

    def __str__(self):
        return f'{self.name}'


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom django user.
    Password and email are required. Other fields are optional.
    """

    ###################
    # REQUIRED FIELDS #
    ###################
    full_name = models.CharField(_('full name'), max_length=30)
    email = models.EmailField(_('email address'), unique=True)
    ###################
    # OPTIONAL FIELDS #
    ###################
    # generic optional fields
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the '
                                               'user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user '
                                                'should be treated as '
                                                'active. Unselect this '
                                                'instead of deleting '
                                                'accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=tz.now)

    # registration fields
    registration_code = models.UUIDField(default=uuid.uuid4,
                                         editable=False)
    email_verified = models.BooleanField(default=False)
    #######################################################

    organizations = models.ManyToManyField(Organization)
    # default organization for user.
    default_organization = models.ForeignKey(Organization,
                                             on_delete=models.CASCADE,
                                             related_name='default_user_set')
    objects = managers.UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['full_name', 'email']

    def get_full_name(self):
        """Return the first_name plus the last_name."""
        return self.full_name

    def get_short_name(self):
        """Return the short name for the user."""
        return self.full_name

    def send_email(self, subject, message, from_email=None, **kwargs):
        """Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def create_default_organization(self):
        organization_name = self.email
        organization_slug = get_slug(Organization.objects.all(),
                                     self.email.split('@')[0])
        organization = Organization.objects.create(
            name=organization_name,
            slug=organization_slug,
        )
        return organization

    def save(self, *args, **kwargs):
        is_created = not self.pk
        if is_created:
            full_name = kwargs.get('full_name', self.full_name)
            if not self.default_organization:
                # create default organization.
                slug = get_slug(Organization.objects.all(), full_name)
                organization = Organization.objects.create(email=self.email,
                                                           name=self.full_name,
                                                           slug=slug)
                logger.warning('No organization is provided. Default '
                               f'organization is created with slug {slug}')
                self.default_organization = organization
        result = super().save(*args, **kwargs)
        if is_created:
            self.organizations.add(self.default_organization)
        return result


class Project(TimeStampedModel):
    slug = models.SlugField()
    name = models.CharField(max_length=255, blank=True, null=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
        ]

        unique_together = [
            ('slug', 'organization')
        ]
