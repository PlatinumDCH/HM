from django.shortcuts import render

# Create your views here.

def register_and_login(request):
    return render(request,'user_room/register_login.html', context={'text':'Register and loging page'})