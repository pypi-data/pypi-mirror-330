"""
send_notifications for :mod:`django_notifications.management.commands` application.

:creationdate:  07/01/2022 08:33
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications.management.commands.send_notifications
"""

import logging
from typing import Any

from django.core.management.base import BaseCommand
from django.utils import timezone

from django_notifications import models

__author__ = "fguerin"
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Send notifications command."""

    def handle(self, *args: Any, **options: Any) -> str | None:
        """Send email notifications."""
        sent = 0
        for notification in models.Notification.objects.filter(sent_at__isnull=True).filter(
            delayed_sending_at__lte=timezone.now()
        ):
            sent += notification.send()
        self.stderr.write(f"{sent} notifications sent.\n")
