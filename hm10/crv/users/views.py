from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm



def register_and_login(request):

    registration_form = RegisterForm()
    login_form = LoginForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            registration_form  =  RegisterForm(request.POST)
            if registration_form.is_valid():
                user = registration_form.save()
                login(request, user)
                return redirect('quotes:home') # перенаправление на домашнюю страницу

        elif 'login' in request.POST:
            login_form = LoginForm(request, request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('quotes:home')

    context = {
        'registration_form': registration_form,
        'login_form': login_form,
    }
    return render(request, 'users/register_login.html', context)
