from django.shortcuts import render
from .models import Quotes
from django.core.paginator import Paginator


def home_page(request):
    quotes = Quotes.objects.all()
    return render(request, 'quotes/home.html', {'quotes':quotes})

def search(request):
    context = {
        'query': None,
        'results': [],  # Пока результатов нет
    }
    return render(request, 'quotes/search_results.html', context)