try:
    from django.utils.timezone import now  # Django 1.4 aware datetimes
except ImportError:
    from datetime import datetime
    now = datetime.now


def broadcast(recipients_qs, msg_instance, *args, **kwargs):
    ThruModel = msg_instance._meta.get_field('recipients').rel.through
    ThruModel.objects.bulk_create(
        ThruModel(
            message=msg_instance,
            user=recipient,
            *args,
            **kwargs
        )
        for recipient in recipients_qs
    )


def get_messages(user, mark_read=True):
    """
    Returns the messages for user.

    By default marks any unread messages as read. This makes sense if you
    display the whole message to the user, if you only show subject lines
    then pass `mark_read=False` and mark messages as read manually when
    they are opened.
    """
    if mark_read:
        user.antenna_messages.update(read_at=now())
    return user.antenna_messages.all()
