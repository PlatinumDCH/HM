from django.shortcuts import render, get_object_or_404
from .models import Quotes, Author
from django.db.models import Q
from django.core.paginator import Paginator


def home_page(request, page=1):

    quotes = Quotes.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    return render(request, 'quotes/home.html', {'quotes':quotes_on_page})

def search(request):
    query = request.GET.get('q', '')
    quotes = []

    if query:
        quotes = Quotes.objects.filter(
            Q(tags__icontains=query)
        ).distinct()

    context = {
        'query': query,
        'quotes': quotes,
    }
    return render(request, 'quotes/search_results.html', context)
