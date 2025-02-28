import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    user_id = models.UUIDField(_("unique user id"), unique=True, default=uuid.uuid4)
    last_modified = models.DateTimeField(auto_now=True, null=False)
