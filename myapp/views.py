from django.shortcuts import render

# Create your views here.
# views.py


def landing(request):
    return render(request, 'landingpage.html')
