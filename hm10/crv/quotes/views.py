from django.shortcuts import render
from .models import Quotes
from django.core.paginator import Paginator


def home_page(request, page=1):

    quotes = Quotes.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    return render(request, 'quotes/home.html', {'quotes':quotes_on_page})

def search(request):
    context = {
        'query': None,
        'results': [],  # Пока результатов нет
    }
    return render(request, 'quotes/search_results.html', context)