from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order


@receiver(post_save, sender=Order)
def listing_delete_on_order_create(sender, instance, created, **kwargs):
    if not created:
        return

    listing = instance.product
    if listing and not listing.is_hidden:
        listing.is_hidden = True
        listing.save(update_fields=['is_hidden'])

