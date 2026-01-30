from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_prometheus.models import ExportModelOperationsMixin


class User(ExportModelOperationsMixin("user"), AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    profile_picture = models.ImageField(upload_to="profiles/", null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)

    # Use email instead of username for login if desired, but
    # we'll keep username for now as well since it's required by AbstractUser.
    # To use email as primary login, uncomment below:
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
