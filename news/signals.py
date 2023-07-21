from django.db.models.signals import m2m_changed
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from .models import PostCategory
from .tasks import new_post_to_subscribes, welcome_letter


# Срабатывает, когда добавили новость
@receiver(m2m_changed, sender=PostCategory)
def sending_message_to_subscribed_users(sender, instance, **kwargs):
    if kwargs['action'] == "post_add":
        new_post_to_subscribes(instance)


# Срабатывает при регистрации пользователя
@receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def user_signed_up_(request, user, **kwargs):
    welcome_letter(user)
