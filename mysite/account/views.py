from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from .forms import (
    RegistrationForm,
    AccountAuthenticationForm,
    UpdateAccountForm,
)

# Create your views here.

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            account = form.save()
            login(request, account)

            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)

    return redirect('home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(email=email, password=password)
            login(request, user)

            if user:
                login(request, user)
                return redirect('home')

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, 'account/login.html', context)

def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}

    if request.POST:
        form = UpdateAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial={
                'email': request.POST['email'],
                'username' : request.POST['username'],
            }
            form.save()
            context['success_message'] = "Updated!"
    else:
        form = UpdateAccountForm(
            initial={
                'email' : request.user.email,
                'username' : request.user.username,
            }
        )

    context['account_form'] = form
    return render(request, 'account/account.html', context)