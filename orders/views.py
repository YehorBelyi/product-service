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
        order = Order.objects.get_or_create(
            product=get_object_or_404(Listing, pk=kwargs.get('product_id')),
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address1=request.POST.get('address1'),
            address2=request.POST.get('address2'),
            city=request.POST.get('city'),
            country=request.POST.get('country'),
            postal_code=request.POST.get('postal_code'),
            phone=request.POST.get('phone'),
        )[0]

        try:
            checkout_session = create_checkout_session(order)
            return redirect(checkout_session.url)
        except Exception as e:
            print(e)
            request.session['payment_error'] = str(e)
            return redirect('order_cancel')

class OrderConfirmationView(View):
    template_name = 'orders/order_confirm.html'

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Listing, id=kwargs.get('product_id'))
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        country = request.POST.get('country')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        context = {
            'listing': product,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'address1': address1,
            'address2': address2,
            'city': city,
            'postal_code': postal_code,
            'country': country,
        }
        return render(request, self.template_name, context=context)


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

class OrderCreateView(LoginRequiredMixin, View):
    template_name = 'orders/order_create.html'

    def get(self, request, *args, **kwargs):
        form = OrderForm(request.GET or None)
        product = get_object_or_404(Listing, pk=kwargs.get('product_id'))
        images = product.product_images.all()
        context = {
            "form": form,
            "listing": product,
            'main_image': images[0],
        }
        return render(request, self.template_name, context=context)

class OrderConfirmCancelView(View):
    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        error = "Payment was cancelled by the user."
        request.session['payment_error'] = error
        return redirect('order_cancel')