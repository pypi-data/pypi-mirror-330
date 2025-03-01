"""
notifications_tags for :mod:`django_notifications.templatetags` application.

:creationdate: 31/03/2022 15:08
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications.templatetags.notifications_tags
"""

import logging
import warnings

from django import template
from django.utils.safestring import SafeString, mark_safe

register = template.Library()
__author__ = "fguerin"
logger = logging.getLogger(__name__)


@register.filter(name="split")
def split(value, arg):
    """
    Split a string by a separator.

    :param value: The string to split
    :param arg: The separator
    :return: The splited string
    """
    return value.split(arg)


@register.simple_tag(name="spaces", takes_context=False)
def get_spaces(count: int = 4) -> SafeString:
    """
    Return a string of spaces.

    :param count: Number of spaces
    :return: String of spaces
    """
    warnings.warn("`spaces` is deprecated, use `ljust` filter instead", DeprecationWarning)  # noqa: B028
    return mark_safe(" " * count)  # noqa: S308
