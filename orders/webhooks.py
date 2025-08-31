import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Order
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order_id = session.get('client_reference_id')
                order = Order.objects.get(id=order_id)
                order.is_paid = True
                order.save()

            except Order.DoesNotExist:
                return HttpResponse(status=404)
            except ValueError:
                return HttpResponse(status=400)

    return HttpResponse(status=200)