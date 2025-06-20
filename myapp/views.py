
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import EngineerRegisterForm, CustomerRegisterForm
from .models import EngineerProfile, CustomerProfile,EngineerScreening
from django.contrib.auth.models import User


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def save_screening_data(request):
    if request.method == 'POST':
        data = request.POST
        EngineerScreening.objects.create(
            email=data.get('email'),
            experience=data.get('experience'),
            project_type=data.get('project_type'),
            tools=data.get('tools'),
            q1=data.get('q1'),
            q2=data.get('q2'),
            q3=data.get('q3'),
        )
        return JsonResponse({'status': 'saved'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def register_engineer(request):
    if request.method == 'POST':
        form = EngineerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            EngineerProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                skills=form.cleaned_data['skills']
            )

            login(request, user)
            return redirect('engineer_dashboard')
    else:
        form = EngineerRegisterForm()

    return render(request, 'register_engineer.html', {'form': form})


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            CustomerProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )

            login(request, user)
            return redirect('customer_dashboard')
    else:
        form = CustomerRegisterForm()

    return render(request, 'register_customer.html', {'form': form})



def landing(request):
    return render(request, 'landingpage.html')

def customer_dash(request):
    return render(request, 'customer_dashboard.html')

def engineer_dash(request):
    return render(request, 'engineer_dashboard.html')

def engineer_apply(request):
    context = {
        "EMAILJS_PUBLIC_KEY": settings.EMAILJS_PUBLIC_KEY,
        "EMAILJS_SERVICE_ID": settings.EMAILJS_SERVICE_ID,
        "EMAILJS_TEMPLATE_ID": settings.EMAILJS_TEMPLATE_ID,
    }
    return render(request, 'engineer_apply.html',context)
