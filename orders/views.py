from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.edit import CreateView

from ProductService.models import Listing, ProductImages
from .forms import OrderForm

from .models import Order
from .services import create_checkout_session


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

class OrderSuccessView(View):
    template_name = 'orders/order_success.html'

    def get(self, request):
        order_id = request.GET.get("order_id")
        return render(request, self.template_name, {"order_id": order_id})


class OrderCancelView(View):
    template_name = 'orders/order_cancel.html'

    def get(self, request):
        error = request.session.pop('payment_error', None)
        context = {
            "error": error,
        }
        return render(request, self.template_name, context=context)

class OrderCreateView(LoginRequiredMixin, CreateView):
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
        images = product.product_images.all()
        context['listing'] = product
        context['main_image'] = images[0]
        return context

class OrderConfirmCancelView(View):
    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        error = "Payment was cancelled by the user."
        request.session['payment_error'] = error
        return redirect('order_cancel')