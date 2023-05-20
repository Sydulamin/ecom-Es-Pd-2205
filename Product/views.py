from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from sslcommerz_lib import SSLCOMMERZ

from .models import *


def product_details(request, id):
    user = request.user
    if user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user)
        cart_len = len(cart_obj)
    prod = Product.objects.get(id=id)
    qun1 = request.GET.get('quantity')
    if qun1:
        qun = int(qun1)
        try:
            prod = Product.objects.get(id=id)
            if prod:
                if prod.quantity != None:
                    if qun > prod.quantity:
                        messages.success(request, 'Product Quantity is not available')
                        return redirect('home')
                    else:
                        new_prod_quantity = prod.quantity - qun
                        prod.quantity = new_prod_quantity
                        prod.save()
                else:
                    messages.success(request, 'Product Quantity is not available')
        except Product.DoesNotExist:
            return HttpResponseBadRequest('Invalid Product Id')

        cartProd = [p for p in Cart.objects.all() if p.user == user]
        if cartProd:
            total = 0.00
            for p in cartProd:
                totalAmount = (p.quantity) * (p.product.price)
                total = total + totalAmount
        if user.is_authenticated:
            try:
                cart = Cart.objects.get(Q(user=user, product=prod))
                cart.quantity += qun
                cart.save()
            except Cart.DoesNotExist:
                Cart.objects.create(user=user, product=prod, quantity=qun)
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'Product/shop-product-full.html', locals())


def addtoCart(request, id):
    user = request.user
    try:
        prod = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return HttpResponseBadRequest('Invalid Product Id')

    cartProd = [p for p in Cart.objects.all() if p.user == user]
    if cartProd:
        total = 0.00
        for p in cartProd:
            totalAmount = (p.quantity) * (p.product.price)
            total = total + totalAmount

    if user.is_authenticated:
        try:
            cart = Cart.objects.get(Q(user=user, product=prod))
            cart.quantity += 1
            cart.save()
        except Cart.DoesNotExist:
            Cart.objects.create(user=user, product=prod)
        return redirect('home')
    else:
        return redirect('login')
    return redirect('home')


def remove_from_cart(r, id):
    remove_product = Cart.objects.get(id=id)
    remove_product.delete()
    return redirect('home')


def cartPage(request):
    user = request.user
    cartProd = [p for p in Cart.objects.all() if p.user == user]
    if cartProd:
        shipping_cost = 100
        total = 0.00
        for p in cartProd:
            totalAmount = (p.quantity) * (p.product.price)
            total = total + totalAmount
            totalwithSHipping = total + shipping_cost

    if user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user)
        cart_len = len(cart_obj)
    prod_Cart = Cart.objects.filter(user=request.user)

    return render(request, 'Product/cart.html', locals())


def update_quantity(request, product_id, action):
    product = Cart.objects.get(product=product_id, user=request.user)
    if action == 'plus':
        product.quantity += 1

    elif action == 'minus':
        if product.quantity > 0:
            product.quantity -= 1

        else:
            product.delete()
            return redirect('home')
    product.save()
    return redirect('cartPage')


def CheckOut(request):
    user = request.user
    cartProd = [p for p in Cart.objects.all() if p.user == user]
    if cartProd:
        shipping_cost = 100
        total = 0.00
        for p in cartProd:
            totalAmount = (p.quantity) * (p.product.price)
            total = total + totalAmount
            totalwithSHipping = total + shipping_cost

    if user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user)
        cart_len = len(cart_obj)
    prod_Cart = Cart.objects.filter(user=request.user)
    return render(request, 'Product/checkout.html', locals())


def sslcommerz_success(request):
    return render(request, 'success.html')

def sslcommerz_fail(request):
    return render(request, 'fail.html')


def sslcommerz_payment(request):
    user = request.user
    cartProd = [p for p in Cart.objects.all() if p.user == user]
    if cartProd:
        shipping_cost = 100
        total = 0.00
        for p in cartProd:
            totalAmount = (p.quantity) * (p.product.price)
            total = total + totalAmount
            totalwithSHipping = total + shipping_cost


    sslcz = SSLCOMMERZ({'store_id': 'niyam6412dc52e1e89', 'store_pass': 'niyam6412dc52e1e89@ssl', 'issandbox': True})
    total_amount = request.GET.get('totalwithSHipping')
    print(total_amount)

    data = {
        'total_amount': totalwithSHipping,
        'currency': "BDT",
        'tran_id': "tran_12345",
        'success_url': "http://127.0.0.1:8000/payment/success/",
        # if transaction is succesful, user will be redirected here
        'fail_url': "http://127.0.0.1:8000/payment/fail/",  # if transaction is failed, user will be redirected here
        # 'cancel_url': "http://127.0.0.1:8000/payment-cancelled",
        # after user cancels the transaction, will be redirected here
        'emi_option': "0",
        'cus_name': "test",
        'cus_email': "test@test.com",
        'cus_phone': "01700000000",
        'cus_add1': "customer address",
        'cus_city': "Dhaka",
        'cus_country': "Bangladesh",
        'shipping_method': "NO",
        'multi_card_name': "",
        'num_of_item': 1,
        'product_name': "Test",
        'product_category': "Test Category",
        'product_profile': "general",
    }

    response = sslcz.createSession(data)
    return redirect(response['GatewayPageURL'])
