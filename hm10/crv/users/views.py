from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from typing import Any

from .forms import RegisterForm, LoginForm
from quotes.forms import QuoteForm       # type: ignore
from quotes.models import Quotes, Author # type: ignore
from .models import Profile

def register_and_login(request: HttpRequest)->HttpResponse:
    registration_form = RegisterForm()
    login_form = LoginForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            registration_form  =  RegisterForm(request.POST)
            if registration_form.is_valid():
                user = registration_form.save()
                login(request, user)
                return redirect('quotes:home')

        elif 'login' in request.POST:
            login_form = LoginForm(request, request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('quotes:home')

    context:dict[str, Any] = {
        'registration_form': registration_form,
        'login_form': login_form,
    }
    return render(request, 'users/register_login.html', context)

def logout_view(request: HttpRequest)->HttpResponse:
    logout(request)
    return redirect('quotes:home')

def account_pages(request):
    return render(request, 'users/account.html',context={})

@login_required
def account_pages(request: HttpRequest)->HttpResponse:
    # create profile if not yet
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            author_name = form.cleaned_data.get('new_author')
            if author_name:  # if input new author
                author, created = Author.objects.get_or_create(fullname=author_name)
                quote.author = author
            elif not quote.author:  # if author not input
                # process default value author
                author, created = Author.objects.get_or_create(fullname=request.user.username)
                quote.author = author

            quote.save()
            request.user.profile.added_quotes.add(quote)
            return redirect('users:account')
    else:
        form = QuoteForm()

    quotes = request.user.profile.added_quotes.all()
    return render(request, 'users/account.html', {'form': form, 'quotes': quotes})
