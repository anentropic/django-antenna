from .models import Message, STATUS_PENDING, STATUS_ACCEPTED


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
