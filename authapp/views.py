from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegistrationForm, ShopUserEditForm
from django.contrib import auth
from django.urls import reverse
from basketapp.models import Basket
from logger.logger_config import log


@log('Log in page is active')
def login(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))
    else:
        login_form = ShopUserLoginForm()
    content = {
        'login_form': login_form,
        'basket': basket,
        'next': next
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


@log('Registration page is active')
def register(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    if request.method == 'POST':
        register_form = ShopUserRegistrationForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegistrationForm()
    content = {'register_form': register_form, 'basket': basket}
    return render(request, 'authapp/register.html', content)


@log('Editing page is active')
def edit(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
    content = {'edit_form': edit_form, 'basket': basket}
    return render(request, 'authapp/edit.html', content)
