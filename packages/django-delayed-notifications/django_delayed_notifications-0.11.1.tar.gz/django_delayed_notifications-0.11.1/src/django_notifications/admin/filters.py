"""
Filters for :mod:`django_notifications.admin` application.

:creationdate: 24/01/2022 14:19
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications.admin.filters
"""

import logging
from typing import Any

from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

__author__ = "fguerin"

from django_notifications import models

logger = logging.getLogger(__name__)


class SentMessageListFilter(SimpleListFilter):
    """Filter messages by sent status."""

    title = _("Sent status")
    parameter_name = "sent"

    def lookups(self, request: HttpRequest, model_admin: Any) -> tuple[tuple[str, str], ...]:
        """
        Return a list of tuples.

        :return: Tuple of tuples
        """
        return (
            ("sent", _("Sent notifications")),
            ("unsent", _("Unsent notifications")),
        )

    def queryset(self, request: HttpRequest, queryset: QuerySet[models.Notification]) -> QuerySet[models.Notification]:
        """
        Return the filtered queryset.

        :param request: HTTP Request
        :param queryset: queryset
        :return: Filtered queryset
        """
        if self.value() == "sent":
            return queryset.filter(sent_at__isnull=False)
        if self.value() == "unsent":
            return queryset.filter(sent_at__isnull=True)
        return queryset  # no filter


class DelayedMessageListFilter(SimpleListFilter):
    """Filter messages by delayed status."""

    title = _("Delayed status")
    parameter_name = "delayed"

    def lookups(self, request: HttpRequest, model_admin: Any) -> tuple[tuple[str, str], ...]:
        """
        Return a list of tuples.

        :param request: HTTP request
        :param model_admin: model admin
        :return: Tuple of tuples

        """
        return (
            ("delayed", _("Delayed notifications")),
            ("undelayed", _("Immediate notifications")),
        )

    def queryset(self, request: HttpRequest, queryset: QuerySet[models.Notification]) -> QuerySet[models.Notification]:
        """
        Return the filtered queryset.

        :param request: HTTP request
        :param queryset: queryset
        :return: Filtered queryset
        """
        if self.value() == "delayed":
            return queryset.filter(delayed_sending_at__isnull=False)
        if self.value() == "undelayed":
            return queryset.filter(delayed_sending_at__isnull=True)
        return queryset  # no filter
