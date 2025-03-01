"""
Apps for :mod:`django_notifications` application.

:creationdate:  07/01/2022 10:33
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications.apps
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoNotificationsConfig(AppConfig):
    """AppConfig for :mod:`django_notifications` application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_notifications"
    verbose_name = _("Notifications")
