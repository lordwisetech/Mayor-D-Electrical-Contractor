from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
# Create your views here.
# views.py


def landing(request):
    return render(request, 'landingpage.html')





from .forms import EngineerSignupForm
from .models import Engineer

def engineer_signup(request):
    if request.method == 'POST':
        form = EngineerSignupForm(request.POST, request.FILES)
        if form.is_valid():
            engineer = form.save(commit=False)
            engineer.set_password(form.cleaned_data['password'])
            engineer.save()
            return redirect('engineer_login')  
    else:
        form = EngineerSignupForm()

    return render(request, 'engineer_signup.html', {'form': form})


def engineer_directory(request):
    engineers = Engineer.objects.all()
    return render(request, 'engineer_directory.html', {'engineers': engineers})






def engineer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('engineer_directory')  # You can change this
        else:
            return render(request, 'engineer_login.html', {'error': 'Invalid login credentials'})
    return render(request, 'engineer_login.html')