"""
config for :mod:`django_notifications.models` application.

:creationdate: 31/03/2022 11:53
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications.models.config
"""

import logging

__author__ = "fguerin"

from django.db import models
from django.utils.translation import gettext as _
from solo.models import SingletonModel

logger = logging.getLogger(__name__)


class NotificationConfig(SingletonModel):
    """Configuration for the notifications."""

    #: If set, the notification will be delayed and sent through a cron job
    delay_notifications = models.BooleanField(
        verbose_name=_("Delay notifications"),
        default=False,
        help_text=_("Delay the notifications, using a cron job."),
    )

    #: Delay to apply to the notifications
    delay = models.PositiveIntegerField(
        verbose_name=_("Delay"),
        default=0,
        help_text=_("Delay in seconds."),
    )

    #: If set, the notification will be sent to the user.
    receive_notifications_field = models.CharField(
        verbose_name=_("Blocking notifications field"),
        max_length=255,
        default="userprofile.receive_notifications",
        help_text=_("Field to check if the user wants to receive notifications."),
    )

    #: If set, the messages will be sent to the user.
    receive_messages_field = models.CharField(
        verbose_name=_("Blocking messages field"),
        max_length=255,
        default="userprofile.receive_messages",
        help_text=_("Field to check if the user wants to receive messages."),
    )

    enable_debug_notifications = models.BooleanField(
        verbose_name=_("Enable debug notifications"),
        default=False,
        help_text=_("If enabled, notification copies will be sent to the provided email."),
    )

    debug_notifications_email = models.EmailField(
        verbose_name=_("Debug notifications email"),
        blank=True,
        default="",
        help_text=_("Email to send the notification copies to."),
    )

    class Meta:
        """Metaclass."""

        verbose_name = _("Notification configuration")
        verbose_name_plural = _("Notification configurations")

    def __str__(self):
        """Get the string representation."""
        return _("Notification configuration")
