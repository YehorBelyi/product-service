from django.urls import path
from .views import CreateCheckoutSessionView, OrderSuccessView, OrderCancelView, OrderCreateView, stripe_webhook_view, \
    OrderConfirmationView, OrderConfirmCancelView

urlpatterns = [
    path('create-checkout-session/<int:order_id>', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('create/<int:product_id>', OrderCreateView.as_view(), name='create-order'),
    path('success/', OrderSuccessView.as_view(), name='order_success'),
    path('cancel/', OrderCancelView.as_view(), name='order_cancel'),
    path('confirm/<int:order_id>', OrderConfirmationView.as_view(), name='confirm-order'),
    path('webhooks/stripe/', stripe_webhook_view, name='stripe-webhook'),
    path('cancel/<int:order_id>', OrderConfirmCancelView.as_view(), name='order-confirm-cancel'),
]