# Notifications

This application sends notifications to the user and emails addresses.
It stores messages into a database, and sends can be delayed through a cron task.

## Installation

```shell
$ pip install django-delayed-notifications
```

Add `django_notifications` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    "django_notifications",
    ...
)
```

Apply the migrations:

```shell
$ ./manage.py migrate
```

## Usage

Instead of sending a raw email, with the `send_mail` django function, you can create a Notification object and program
the sending.

### Notification creation

```python
from pathlib import Path
from django_notifications.models import Notification, Attachment
from django.core.files import File
from django.utils.timezone import now
from datetime import timedelta

# **Basic creation**
my_instance = "<A random object in the application>"
notification = Notification.objects.create(
    subject="My beautiful email",
    text_body="My text body",
    html_body="""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="x-apple-disable-message-reformatting">
    <title>My beautiful email</title>
</head>
<body>My HTML body</body>
</html>
    """,
    from_email="foo@example.org",  # Optional

)

# ** Related objects management **
# It is possible to attach an object to the email (Optional)
notification.related_object = my_instance

# ** Related objects states management **
# When using FSM, you can provide the states from / to (Optional)
notification.state_from = "active"
notification.state_to = "processing"

# **Attachments management**
_attachment = Attachment.objects.create(
    notification=notification,
    attachment_file=File(Path("<my_file>").open("r"), name="my_file.txt")
)

# **Recipients management**
# You can provide users
notification.recipients.set("<User instance>", "<User instance>", ...)
notification.save()

# And / Or provides email address, `\n` separated
notification.email_recipients = "\n".join([
    "foo@example.org", "bar@example.org"
])
notification.save()

# You can set the delayed sending date
notification.delayed_sending_at = now() + timedelta(days=1)
notification.save()

# Or you can send the email immediately
notification.send()
```

### Management command

The application provides a management command to send the emails:

```sh
$ ./manage.py send_notifications
12 notifications sent.
```

### Templates

The application provides some basic templates for emails.

### Admin

This application provides an admin interface for notifications.

## Notes

The application is available in English and translated to French.
