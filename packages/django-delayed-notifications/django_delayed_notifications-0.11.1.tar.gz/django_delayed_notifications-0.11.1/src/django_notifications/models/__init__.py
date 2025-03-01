"""
Models for :mod:`django_notifications application`.

:creationdate: 06/01/2022 11:31
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications.models
"""

import logging
import mimetypes
import pprint
from datetime import timedelta
from functools import cached_property

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models.fields.files import FieldFile
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _
from django_currentuser.middleware import get_current_authenticated_user

from . import config, helpers

__author__ = "François GUÉRIN"
logger = logging.getLogger(__name__)


def filter_receive_notification(user: User) -> bool:
    """
    Filter users allowing to receive notification.

    :param user: User to filterS
    """
    _config = config.NotificationConfig.get_solo()
    _receive_notifications_field = _config.receive_notifications_field
    split = _receive_notifications_field.split(".")
    try:
        if len(split) == 1:
            _receive_notifications = getattr(user, _receive_notifications_field)
        else:
            _receive_notifications_profile = getattr(user, split[0])
            _receive_notifications = getattr(_receive_notifications_profile, split[1])
        logger.debug("filter_receive_notification(%s) %s", user, _receive_notifications)
        return _receive_notifications
    except AttributeError:
        logger.debug("filter_receive_notification(%s) No profile found !", user)
        return True


def filter_receive_messages(user) -> bool:
    """
    Filter users allowing to receive messages.

    :param user: User to filterS
    """
    _config = config.NotificationConfig.get_solo()
    _receive_messages_field = _config.receive_messages_field
    split = _receive_messages_field.split(".")
    try:
        if len(split) == 1:
            _receive_messages = getattr(user, _receive_messages_field)
        else:
            _receive_messages_profile = getattr(user, split[0])
            _receive_messages = getattr(_receive_messages_profile, split[1])
        logger.debug("filter_receive_messages(%s) %s", user, _receive_messages)
        return _receive_messages
    except AttributeError:
        logger.debug("filter_receive_message(%s) No profile found !", user)
        return True


class Attachment(models.Model):
    """Attachment for a notification."""

    #: The notification to attach the file to
    notification = models.ForeignKey(
        "django_notifications.Notification",
        on_delete=models.CASCADE,
        related_name="attachments",
    )

    #: The file to attach
    attachment_file = models.FileField(
        upload_to="notifications/attachments/%Y/%m/%d/",
    )

    class Meta:
        """Metaclass."""

        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")
        ordering = ("notification", "id")

    def __str__(self):
        """Get a string representation of the attachments."""
        return _("{attachment_file_name} for {notification}").format(
            attachment_file_name=self.attachment_file.name,
            notification=self.notification,
        )


class Notification(models.Model):
    """Model for :class:`django_notifications.models.Notification`."""

    # region Fields
    #: The user who created the notification
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        default=1,
        editable=False,
        verbose_name=_("Created by"),
    )

    #: notification creation date
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Created at"),
    )

    #: Optional delayed notification date
    delayed_sending_at = models.DateTimeField(
        verbose_name=_("Delayed sending at"),
        null=True,
        blank=True,
    )

    #: Effective notification sending date
    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Sent at"),
    )

    #: Notification subject
    subject = models.CharField(
        max_length=255,
        verbose_name=_("Subject"),
    )

    #: Notification text content
    text_body = models.TextField(
        verbose_name=_("Text body"),
    )

    #: Notification html content
    html_body = models.TextField(
        verbose_name=_("HTML body"),
    )

    #: Notification related object content type
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    #: Notification related object identifier
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    #: Notification related object
    related_object = GenericForeignKey(
        "content_type",
        "object_id",
    )

    #: Notification object transition from state
    state_from = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("State from"),
    )

    #: Notification object transition to state
    state_to = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("State to"),
    )

    #: Recipients as users list
    recipients = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Recipients"),
        related_name="notifications",
        blank=True,
    )

    #: Recipients as emails list, one per line
    email_recipients = models.TextField(
        verbose_name=_("Email recipients"),
        blank=True,
        help_text=_("One email per line"),
    )

    #: Email sender
    from_email = models.EmailField(
        verbose_name=_("From email"),
        help_text=_("Email address to use as sender"),
        default=settings.DEFAULT_FROM_EMAIL,
    )

    #: Set recipients as BCC
    as_bcc = models.BooleanField(
        verbose_name=_("As bcc"),
        default=False,
        help_text=_("Email message will be sent as BCC values."),
    )

    # endregion Fields

    class Meta:
        """Metaclass for :class:`django_notifications.models.Notification`."""

        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        """Get a string representation of the notification."""
        return f"{self.subject} - {self.created_by} - {self.created_at}"

    def _set_administrative_data(self):
        """
        Update the administrative fields of the Administrable models.

        .. note:: Hook method.

        :return: Nothing
        """
        current_user = get_current_authenticated_user()
        default_user = apps.get_model(settings.AUTH_USER_MODEL).objects.order_by("pk").first()  # type: ignore
        assert default_user is not None, "No default user found - please create one"  # noqa: S101

        if current_user is None:
            current_user = default_user
            logger.warning(
                "%s::_set_administrative_data() Unable to get the current user from local thread: "
                'setting the default one: "%s"',
                self.__class__.__name__,
                current_user,
            )

        # Looks like as nn instance creation
        if self.pk is None:
            self.created_by = current_user or default_user
            logger.info(
                "%s::_set_administrative_data() Creates a new instance (%s): created_by = %s",
                self.__class__.__name__,
                self,
                self.created_by,
            )

    def save_base(
        self,
        raw=False,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ) -> None:
        """
        Save the connected user into the right field, according to the object state.

        + If the object is a new one: :attr:`django_notifications.models.Notification.created_by`
          is set to the current user.

        :param raw: Raw SQL query ?
        :param force_insert: Force insertion
        :param force_update: Force update
        :param using:  DB alias used
        :param update_fields: List fields to update
        :return: Nothing
        """
        self._set_administrative_data()

        super().save_base(
            raw=raw,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def get_recipients(self) -> list[str]:
        """Get **ALL** recipients for the email."""
        _recipients = []
        if self.email_recipients:
            _email_recipients = self.email_recipients
            if isinstance(_email_recipients, list):
                _recipients.extend(_email_recipients)
            elif isinstance(_email_recipients, str):
                _additional_recipients = [r.strip() for r in _email_recipients.split("\n") if r.strip()]
                _recipients.extend(_additional_recipients)
            else:
                logger.warning(
                    "%s::get_recipients() self.email_recipients not recognized: %s (%s)",
                    self.__class__.__name__,
                    self.email_recipients,
                    _email_recipients.__class__.__name__,
                )

        # Add the recipients from users, filtered by authorization
        if self.recipients.count() > 0:  # noqa
            filtered_users = filter(filter_receive_notification, self.recipients.all())  # noqa
            _users = list(filtered_users)
            logger.debug(
                "%s::get_recipients() Filtered recipients: %s",
                self.__class__.__name__,
                pprint.pformat(_users),
            )
            _recipients.extend([user.email for user in _users])

        logger.info(
            "%s::get_recipients() Final recipient emails: %s",
            self.__class__.__name__,
            pprint.pformat(_recipients),
        )
        return _recipients

    @cached_property
    def email(self) -> EmailMultiAlternatives:
        """
        Get the email message.

        :return: Email message
        """
        recipients = self.get_recipients()

        kwargs = {
            "subject": self.subject,
            "body": self.text_body,
            "from_email": self.from_email or settings.DEFAULT_FROM_EMAIL,
        }

        if self.as_bcc:
            _to = self.from_email or settings.DEFAULT_FROM_EMAIL
            kwargs.update({"bcc": recipients})
            kwargs.update({"to": [_to]})
        else:
            kwargs.update({"to": recipients})

        logger.debug("%s::email() kwargs = %s", self.__class__.__name__, pprint.pformat(kwargs))

        # Create the email message
        email = EmailMultiAlternatives(**kwargs)

        # Add HTML content
        if self.html_body:
            email.attach_alternative(self.html_body, "text/html")

        # Add the attachments (if needed)
        attachments = self.attachments.all()  # noqa
        if attachments.exists():
            for attachment in attachments:
                mime_type, _ = mimetypes.guess_type(attachment.attachment_file.name)
                email.attach_file(path=attachment.attachment_file.path, mimetype=mime_type)
        return email

    @property
    def is_sent(self) -> bool:
        """
        Check if the notification is sent.

        :return: True if the notification is sent, False otherwise
        """
        return self.sent_at is not None

    def _add_attachment(self, attachment_file: FieldFile) -> Attachment:
        """Add a file to the notification."""
        attachment = Attachment.objects.create(  # noqa
            notification=self,
            attachment_file=attachment_file,
        )
        return attachment

    def notify(self, force: bool = False) -> int:
        """
        Notify the user by email.

        :param force: Force the notification
        :return: Number of sent messages
        """
        sent = self.notify_by_email(force=force)
        return sent

    def notify_by_email(self, force: bool = False) -> int:
        """
        Notify the user by email.

        :param force: Force the notification (A notification may be sent many times)
        :return: Number of sent messages
        """
        if self.is_sent and not force:
            logger.info(
                "%s::notify() {self} already sent at {self.sent_at} - skipping",
                self.__class__.__name__,
                self,
                self.sent_at,
            )
            return 0

        _config = config.NotificationConfig.get_solo()
        if _config.delay_notifications:
            logger.info(
                "%s::notify() %s delayed by %s seconds",
                self.__class__.__name__,
                self,
                _config.delay,
            )
            self.delayed_sending_at = timezone.now() + timedelta(seconds=_config.delay)
            return 0
        else:
            # Send the email
            sent = self.send()
            return sent

    def send(self, force: bool = False) -> int:
        """
        Send the email.

        ..note:: Actually send the email notification.

        :param force: Force the notification
        :return: Number of sent messages
        """
        if self.sent_at is not None and not force:
            logger.info(
                "%s::send() %s already sent at %s - skipping",
                self.__class__.__name__,
                self,
                self.sent_at,
            )
            return 0

        sent = self.email.send(fail_silently=False)
        # Update the sent_at field
        self.sent_at = timezone.now()
        self.save()

        # Send e copy of the email if required
        _config = config.NotificationConfig.get_solo()
        if _config.enable_debug_notifications:
            debug_mail = self.get_debug_email(to=_config.debug_notifications_email)
            debug_sent = debug_mail.send(fail_silently=False)
            logger.info(
                "%s::send() DEBUG %s sent %s emails to %s",
                self.__class__.__name__,
                self,
                debug_sent,
                _config.debug_notifications_email,
            )

        logger.info(
            "%s::send() %s sent %s emails for %s recipients",
            self.__class__.__name__,
            self,
            sent,
            self.recipients.count(),  # noqa
        )
        return sent

    def get_debug_email(self, to) -> EmailMultiAlternatives:
        """
        Get the email for debugging purposes.

        :param to: The email address to send the email to
        :return: The email
        """
        email = self.email
        _previous_to = email.to
        _previous_body = email.body
        _previous_html_body = email.alternatives[0][0]
        _new_to = [to]
        _new_body = render_to_string(
            "django_notifications/debug/body.txt.tpl",
            {
                "to": _previous_to,
                "content": _previous_body,
            },
        )
        _new_html_body = helpers.get_debug_html_body(
            html_body=_previous_html_body,
            to=_previous_to,
        )
        # Update the email with new data
        email.to = _new_to
        email.body = _new_body
        email.alternatives = [(_new_html_body, "text/html")]
        email.subject = f"DEBUG {self.subject}"
        return email


def send_mail(subject: str, message: str, from_email: str, recipient_list: list[str]) -> int:
    """Send mail, mocking the django function."""
    notification = Notification.objects.create(
        subject=subject,
        text_body=message,
        from_email=from_email,
        recipient_list=recipient_list,
    )
    return notification.send()
