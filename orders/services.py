import stripe
from django.conf import settings
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(order):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': order.product.product_name,
                },
                'unit_amount': int(order.product.cost * 100),
            },
            'quantity': 1,
        }],
        mode="payment",
        success_url=settings.DOMAIN + reverse('order_success') + f"?order_id={order.id}",
        cancel_url=settings.DOMAIN + reverse('order_cancel'),
        client_reference_id=str(order.id),
    )
    return session