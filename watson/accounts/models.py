from django.db import models

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.core.mail import send_mail
from django.utils import timezone as tz

from accounts import managers


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom django user.
    Password and email are required. Other fields are optional.
    """

    ###################
    # REQUIRED FIELDS #
    ###################
    email = models.EmailField(_('email address'), unique=True)
    ###################
    # OPTIONAL FIELDS #
    ###################
    # generic optional fields
    full_name = models.CharField(_('full name'), max_length=30, blank=True)
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

    # user's state
    email_verified = models.BooleanField(default=False)
    # current users contact.

    #######################################################

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


class Organization(models.Model):

    """Organization Model."""
    # mandatory fields
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255)
    # optional field
    company = models.CharField(max_length=1024, blank=True)
    location = models.CharField(max_length=2048, blank=True)
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)

    users = models.ManyToManyField(User)

    objects = managers.OrganizationManager()

    def __str__(self):
        return f'{self.name}'
