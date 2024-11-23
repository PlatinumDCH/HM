from django.shortcuts import render,HttpResponse

# Create your views here.
def home_page(request):
    return render(request, 'quotes/home.html', {'msg':'Home page'})

def search(request):
    context = {
        'query': None,
        'results': [],  # Пока результатов нет
    }
    return render(request, 'quotes/search_results.html', context)