"""
Tests for :mod:`django_notifications` project.

:creationdate: 01/01/2022 10:46
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications.tests
"""

from django.apps import apps
from django.conf import settings
from django.test import TestCase

from django_notifications import models


class TestDjangoNotifications(TestCase):
    """Test the notification models."""

    def test_creation_with_user(self):
        """Test the creation of a notification."""
        user = apps.get_model(settings.AUTH_USER_MODEL)
        notification = models.objects.create(
            subject="Test",
            text_body="Test",
            html_body="<p>Test</p>",
            recipients=[user],
        )

        self.assertIsNotNone(notification)
        self.assertIsNotNone(notification.created_by)
        self.assertEqual(notification.created_by, user)
        self.assertIs(notification.recipients.all().exists(), True)
