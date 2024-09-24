from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    if created:
        # Notify admins about new order
        admins = User.objects.filter(is_staff=True)
        for admin in admins:
            Notification.objects.create(
                user=admin,
                notification_type='new_order',
                message=f'New order #{instance.id} has been placed.',
                content_object=instance
            )
    else:
        # Notify user about order status change
        Notification.objects.create(
            user=instance.user,
            notification_type=Notification.Type.CHANGE_ORDER,
            message=f'Your order #{instance.id} status has been updated to {instance.status}.',
            content_object=instance
        )
