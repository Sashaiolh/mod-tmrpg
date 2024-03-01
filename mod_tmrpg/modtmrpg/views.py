from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
    
def logout_view(request):
    logout(request)
    return redirect('/') # на главную страницу сайта

def index(request):
    return render(request, 'modtmrpg/index.html')
