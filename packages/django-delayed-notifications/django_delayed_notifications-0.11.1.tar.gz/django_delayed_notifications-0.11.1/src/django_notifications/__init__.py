"""
Application to manage notifications.

.. note::
  This application allow to create notification emains

:copyright: (c) 2022 by François GUÉRIN
:license: mit, see LICENSE for more details.
:creationdate: 06/01/2022 11:31
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications

"""

from django_notifications.models import send_mail

from .__about__ import __version__

VERSION = __version__


__all__ = [
    "__version__",
    "VERSION",
    "send_mail",
]
