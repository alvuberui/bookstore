

from django.urls import path

from . import views

urlpatterns = [
    path('pedido/canceled', views.canceled_pedido, name='index'),
    path('pedido/success', views.success_pedido, name='index'),
    path('pedido/detalles', views.detalles_pedido, name='index'),
    path('pedido/payment/<int:id>', views.payment_book, name='payment'),
    path('pedido/create/', views.create_pedido, name='pedido'),
    path('stripe/config/', views.stripe_config), 
    path('pedido/contrareembolso/<int:id>', views.pago_contrareembolso), 
    path('create-checkout-session/<int:id>', views.create_checkout_session),
]