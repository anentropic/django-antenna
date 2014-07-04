from django.conf import settings
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
try:
    from django.utils.timezone import now  # Django 1.4 aware datetimes
except ImportError:
    from datetime import datetime
    now = datetime.now


SUBJECT_MAX_LENGTH = getattr(settings, 'SUBJECT_MAX_LENGTH', 120)


class BaseMessage(models.Model):
    class Meta:
        abstract = True

    sender = models.ForeignKey(_("sender"), settings.AUTH_USER_MODEL,
                               null=True, blank=True)

    subject = models.CharField(_("subject"), max_length=SUBJECT_MAX_LENGTH)
    body = models.TextField(_("body"), blank=True)


class RecipientsMixin(models.Model):
    class Meta:
        abstract = True

    recipients = models.ManyToMany(_("recipients"), settings.AUTH_USER_MODEL,
                                   through='MessageUser')


class Message(RecipientsMixin, BaseMessage):
    pass


class BaseMessageUser(models.Model):
    class Meta:
        abstract = True

    message = models.ForeignKey('Message')
    user = models.FoerignKey(settings.AUTH_USER_MODEL)

    read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(_("sent at"), default=now)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)


class MessageUser(BaseMessageUser):
    pass
