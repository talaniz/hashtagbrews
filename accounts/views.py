from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, RegisterForm


def login(request):
    """Site main login page."""

    login_form = LoginForm(request.POST or None)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if request.POST['next'] != "":
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('beerdb_main'))
        # TODO: Need to add a redirect with form errors here
    return render(request, 'accounts/login.html', {'form': login_form})


def logout(request):
    auth_logout(request)
    return redirect('index')

def register(request):
    """Site registration form view."""
    register_form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if register_form.is_valid():
            user = register_form.save()
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('beerdb_main'))
    return render(request, 'accounts/register.html', {'form': register_form})
