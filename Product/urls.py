from django.urls import path

from .views import *

urlpatterns = [

    path('product_details/<int:id>/', product_details, name='product_details'),
    path('addtoCart/<int:id>/', addtoCart, name='addtoCart'),
    path('remove_from_cart/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('cartPage/', cartPage, name='cartPage'),
    path('CheckOut/', CheckOut, name='CheckOut'),
    path('update_quantity/<int:product_id>/<str:action>', update_quantity, name='update_quantity'),
    path('payment/', sslcommerz_payment, name="payment"),
    path('payment/success/', sslcommerz_success, name="success"),
    path('payment/fail/', sslcommerz_fail, name="fail"),
]
