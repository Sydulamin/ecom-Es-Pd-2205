from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from Product.models import *


def home(request):
    user = request.user
    if user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user)
        cart_len = len(cart_obj)
    cat_id = request.GET.get('cat_id')
    search = request.GET.get('search')

    cartProd = [p for p in Cart.objects.all() if p.user == user]
    if cartProd:
        total = 0.00
        for p in cartProd:
            totalAmount = (p.quantity) * (p.product.price)
            total = total + totalAmount

    if cat_id:
        p = Product.objects.filter(catagory=cat_id)
    elif search:
        p = Product.objects.filter(name__icontains=search)
    else:
        p = Product.objects.all()

    c = Catagory.objects.all()

    return render(request, 'home.html', locals())


def login_page(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You Are Logged In')
            return redirect('home')
        else:
            messages.error(request, 'Your Username or Password is Incorrect')
            return redirect('login')
    return render(request, 'Accounts/login.html')


def registration_page(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            if User.objects.filter(username=name).exists():
                messages.info(request, 'Username Already Exists , Choose Another one')
                return redirect('reg')
            else:
                user = User.objects.create_user(username=name, email=email, password=password)
                user.set_password(password)
                user.save()
                messages.success(request, 'Log in Success')
                return redirect('login')
        else:
            messages.error(request, 'Please Make Password Same')
            return redirect('reg')
    return render(request, 'Accounts/registration.html')


def log_out(request):
    logout(request)
    messages.success(request, 'Log out Success')
    return redirect('login')


def forget_pass(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['new_pass']
        if name != None:
            user = User.objects.get(username=name)
            print(user)
            print(user.email)
            if user.email == email:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'password change done')
                return redirect('login')
            else:
                messages.error(request, 'email not matched')

    return render(request, 'Accounts/forget_pass.html')


@login_required(login_url='login')
def prof_page(request):
    user = request.user
    if user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user)
        cart_len = len(cart_obj)
    return render(request, 'Accounts/profile.html', locals())
