from django.shortcuts import render

# Create your views here.

def homepage(request):
    return render(request, 'core/home.html')
