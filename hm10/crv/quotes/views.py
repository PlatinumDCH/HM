from django.shortcuts import render
from crv.utils.connect import connect_mongo

# Create your views here.
def home_page(request):
    db = connect_mongo()
    quotes = db.quotes.find()
    return render(request, 'quotes/home.html', {'quotes':quotes})

def search(request):
    context = {
        'query': None,
        'results': [],  # Пока результатов нет
    }
    return render(request, 'quotes/search_results.html', context)