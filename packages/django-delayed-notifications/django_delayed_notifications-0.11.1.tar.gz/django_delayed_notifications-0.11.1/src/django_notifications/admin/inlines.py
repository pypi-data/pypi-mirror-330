"""
inlines for :mod:`django_notifications.admin` application.

:creationdate:  07/01/2022 10:36
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications.admin.inlines
"""

import logging

from django.contrib import admin

from django_notifications import models

__author__ = "fguerin"
logger = logging.getLogger(__name__)


class AttachmentInline(admin.TabularInline):
    """Inline for :class:`django_notifications.models.Attachment`."""

    model = models.Attachment
    extra = 1
