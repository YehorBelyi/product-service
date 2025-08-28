import stripe
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.edit import CreateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from ProductService.models import Listing
from .forms import OrderForm

from .models import Order
from .services import create_checkout_session

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET


# Create your views here.
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)

        try:
            checkout_session = create_checkout_session(order)
            return redirect(checkout_session.url)
        except Exception as e:
            print(e)
            request.session['payment_error'] = str(e)
            return redirect('order_cancel')

class OrderConfirmationView(View):
    template_name = 'orders/order_confirm.html'

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        return render(request, self.template_name, {'order': order})


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
        order_id = session.get('client_reference_id')

        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.status = 'processing'
                order.stripe_payment_intent_id = session.get('stripe_payment_intent_id')
                order.save()
            except Order.DoesNotExist:
                return HttpResponse(status=400)

    return HttpResponse(status=200)


class OrderSuccessView(View):
    template_name = 'orders/order_success.html'

    def get(self, request):
        return render(request, self.template_name)


class OrderCancelView(View):
    template_name = 'orders/order_cancel.html'

    def get(self, request):
        error = request.session.pop('payment_error', None)
        context = {
            "error": error,
        }
        return render(request, self.template_name, context=context)

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_create.html'

    def form_valid(self, form):
        product = get_object_or_404(Listing, pk=self.kwargs['product_id'])
        form.instance.user = self.request.user
        form.instance.product = product
        return super().form_valid(form)

    def get_success_url(self):
        order_id = self.object.pk

        return reverse('confirm-order', kwargs={'order_id': order_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Listing, pk=product_id)
        # main_image = product.p
        context['listing'] = product
        return context