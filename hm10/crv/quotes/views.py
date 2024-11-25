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

    if query:
        quotes = Quotes.objects.filter(
            Q(quote__icontains=query)  |
            Q(tags__icontains=query) |
            Q(author__fullname__icontains = query)
        ).distinct()
    else:
        quotes = Quotes.objects.all()
    return render(request, 'quotes/search_results.html', {'quotes': quotes})

def author_detail(request, id):
    author = get_object_or_404(Author, id=id)
    return render(request, 'quotes/author_detail.html', {'author': author})

def quotes_by_tag(request, tag):

    request.GET = request.GET.copy()
    request.GET['q'] = tag
    return search(request)