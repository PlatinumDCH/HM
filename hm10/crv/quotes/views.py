from django.shortcuts import render,HttpResponse

# Create your views here.
def home_page(request):
    return render(request, 'quotes/home.html', {})

def search(request):
    context = {
        'query': None,
        'results': [],  # Пока результатов нет
    }
    return render(request, 'quotes/search_results.html', context)