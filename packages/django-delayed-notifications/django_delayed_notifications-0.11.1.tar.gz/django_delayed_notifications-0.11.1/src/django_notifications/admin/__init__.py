"""
Models for :mod:`django_notifications application`.

:creationdate: 06/01/2022 11:31
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications.models
"""

import logging

from django.conf import settings
from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.db.models import QuerySet
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext_lazy as _
from solo import admin as solo_admin

import django_notifications.models.config
from django_notifications import models

from . import filters, forms, inlines

logger = logging.getLogger(__name__)
__author__ = "François GUÉRIN"


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin for :class:`django_notifications.models.Notification`."""

    list_display = (
        "get_subject",
        "get_dates",
        "get_related_object",
        "get_states",
        "get_recipients",
    )

    date_hierarchy = "created_at"

    list_filter = [
        filters.SentMessageListFilter,
        filters.DelayedMessageListFilter,
    ]

    inlines = [
        inlines.AttachmentInline,
    ]

    form = forms.NotificationAdminForm

    fieldsets = (
        (
            _("Notification"),
            {
                "fields": (
                    "subject",
                    "text_body",
                    "html_body",
                    "state_from",
                    "state_to",
                )
            },
        ),
        (
            _("Related object"),
            {"fields": ("content_type", "object_id")},
        ),
        (
            _("Recipients"),
            {
                "fields": (
                    "as_bcc",
                    ("recipients", "email_recipients"),
                )
            },
        ),
        (_("Delayed"), {"fields": ("delayed_sending_at",)}),
    )

    search_fields = [
        "email_recipients",
        "recipients__email",
    ]

    # region Permissions
    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Check if user has permission to add a notification.

        .. note:: Always return ``False``.
        """
        return False

    def has_delete_permission(self, request: HttpRequest, obj: models.Notification | None = None) -> bool:
        """
        Check if user has permission to delete a notification.

        .. note:: Return `True` for super users.
        """
        user = request.user
        return user.is_superuser

    # endregion Permissions

    # region List display methods
    @admin.display(description=_("Subject"))
    def get_subject(self, obj: models.Notification) -> SafeString:
        """
        Get the subject and the `sent` status.

        :param obj: The notification object
        :return: The subject and the `sent` status.
        """
        return mark_safe(  # noqa: S308
            render_to_string(
                "django_notifications/admin/snippets/subject.html",
                {
                    "debug": settings.DEBUG,
                    "object": obj,
                },
            )
        )

    @admin.display(description=_("Dates"), ordering="created_at")
    def get_dates(self, obj: models.Notification) -> SafeString:
        """
        Display dates.

        :param obj: :class:`django_notifications.models.Notification` instance
        :return: rendered HTML
        """
        return mark_safe(  # noqa: S308
            render_to_string(
                "django_notifications/admin/snippets/dates.html",
                {
                    "debug": settings.DEBUG,
                    "object": obj,
                },
            )
        )

    @admin.display(description=_("Related object"))
    def get_related_object(self, obj: models.Notification) -> SafeString | None:
        """
        Display related object.

        :param obj: :class:`django_notifications.models.Notification` instance
        :return: rendered HTML
        """
        if obj.related_object:
            _app_label, _app_model_name = obj.related_object._meta.app_label, obj.related_object._meta.model_name  # noqa
            admin_url = reverse_lazy(
                f"admin:{_app_label}_{_app_model_name}_change",
                args=(obj.related_object.pk,),
            )
            return mark_safe(  # noqa: S308
                render_to_string(
                    "django_notifications/admin/snippets/related_object.html",
                    {
                        "debug": settings.DEBUG,
                        "object": obj,
                        "admin_url": admin_url,
                    },
                )
            )
        return None

    @admin.display(description=_("States"), ordering="state_to")
    def get_states(self, obj) -> SafeString:
        """
        Display states.

        :param obj: :class:`django_notifications.models.Notification` instance
        :return: rendered HTML
        """
        return mark_safe(  # noqa: S308
            render_to_string(
                "django_notifications/admin/snippets/states.html",
                {
                    "debug": settings.DEBUG,
                    "object": obj,
                },
            )
        )

    @admin.display(description=_("Recipients"))
    def get_recipients(self, obj) -> SafeString:
        """
        Display recipients.

        :param obj: :class:`django_notifications.models.Notification` instance
        :return: rendered HTML
        """
        return mark_safe(  # noqa: S308
            render_to_string(
                "django_notifications/admin/snippets/recipients.html",
                {
                    "debug": settings.DEBUG,
                    "object": obj,
                },
            )
        )

    # endregion List display methods

    # region Action methods
    @admin.action(description=_("Send notifications"))
    def send_notifications(self, request: HttpRequest, queryset: QuerySet[models.Notification]) -> None:
        """
        Re-send notifications.

        :param request HTTP request
        :param queryset: Selected notifications
        :return: Nothing
        """
        for notification in queryset:
            _sent = notification.notify(force=True)
            if _sent:
                self.message_user(
                    request,
                    message=_("A notification has been sent for {notification}.").format(notification=notification),
                    level="INFO",
                )
            else:
                self.message_user(
                    request=request,
                    message=_("No notification sent for {notification}.").format(notification=notification),
                    level="WARNING",
                )

    @admin.action(description=_("DEBUG - Send notification(s) to the connected user"))
    def send_notification_to_connected_user(self, request: HttpRequest, queryset: QuerySet) -> None:
        """
        Send the email message to the connected user.

        :param request: HTTP Request
        :param queryset: Selected QuerySet
        :return: Nothing
        """
        _user = request.user
        sent = 0
        for notification in queryset:
            _email: EmailMultiAlternatives = notification.email
            _email.to = [_user.email]
            _email.subject = f"[DEBUG] {_email.subject}"
            sent += _email.send(fail_silently=False)
            self.message_user(
                request=request,
                message=_("DEBUG - Email notification sent for {notification} to {user}").format(
                    notification=notification,
                    user=_user,
                ),
                level="INFO",
            )

    actions = [
        send_notifications,
        send_notification_to_connected_user,
    ]
    # endregion Action methods


@admin.register(models.Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    """Admin for :class:`django_notifications.models.Attachment`."""

    list_display = [
        "id",
        "notification",
        "attachment_file",
    ]

    def has_add_permission(self, request: HttpRequest) -> bool:  # noqa
        """
        Don't allow adding attachments.

        :param request: HTTP request
        :return: False
        """
        return False

    def has_delete_permission(self, request: HttpRequest, obj: models.Attachment = None) -> bool:  # noqa
        """
        Don't allow deleting attachments.

        :param request: HTTP request
        :param obj: :class:`django_notifications.models.Attachment` instance
        :return: False
        """
        return False

    def has_change_permission(self, request: HttpRequest, obj: models.Attachment = None) -> bool:  # noqa
        """
        Don't allow changing attachments.

        :param request: HTTP request
        :param obj: :class:`django_notifications.models.Attachment` instance
        :return: False
        """
        return False


@admin.register(django_notifications.models.config.NotificationConfig)
class NotificationConfigAdmin(solo_admin.SingletonModelAdmin):
    """Admin for :class:`django_notifications.models.NotificationConfig`."""

    fieldsets = (
        (
            None,
            {"fields": ("receive_notifications_field", "receive_messages_field")},
        ),
        (
            _("Delayed notifications"),
            {"fields": ("delay_notifications", "delay")},
        ),
        (
            _("Debug"),
            {
                "classes": ("collapse",),
                "fields": ("enable_debug_notifications", "debug_notifications_email"),
            },
        ),
    )
