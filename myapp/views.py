
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import EngineerRegisterForm, CustomerRegisterForm
from .models import EngineerProfile, CustomerProfile,EngineerScreening,CodeShare,Job
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
 

#save screening data
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



#enginerr register
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
                
            )

            login(request, user)
            return redirect('engineer_dashboard')
    else:
        form = EngineerRegisterForm()

    return render(request, 'register_engineer.html', {'form': form})



#customer Register
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
                
            )

            login(request, user)
            return redirect('customer_dashboard')
    else:
        form = CustomerRegisterForm()

    return render(request, 'register_customer.html', {'form': form})


#landing page
def landing(request):
    return render(request, 'landingpage.html')



#customer dashboard

@login_required
def customer_dash(request):
    success = False

    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        description = request.POST.get('description')
        location_name = request.POST.get('location_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if job_title and description and location_name:
            Job.objects.create(
                customer=request.user,
                job_title=job_title,
                description=description,
                location_name=location_name,
                latitude=latitude,
                longitude=longitude
            )
            success = True

    return render(request, 'customer_dashboard.html', {'success': success})

    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        description = request.POST.get('description')
        location_name = request.POST.get('location_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if job_title and description and location_name and latitude and longitude:
            Job.objects.create(
                customer=request.user,
                job_title=job_title,
                description=description,
                location_name=location_name,
                latitude=latitude,
                longitude=longitude
            )
            return redirect('customer_dashboard')  # or wherever you want

    return render(request, 'customer_dashboard.html')

# engineer dashboard view
@login_required
def engineer_dash(request):
    profile = EngineerProfile.objects.filter(user=request.user).first()
    return render(request, 'engineer_dashboard.html', {'profile': profile})


#engineer apply
def engineer_apply(request):
    context = {
        "EMAILJS_PUBLIC_KEY": settings.EMAILJS_PUBLIC_KEY,
        "EMAILJS_SERVICE_ID": settings.EMAILJS_SERVICE_ID,
        "EMAILJS_TEMPLATE_ID": settings.EMAILJS_TEMPLATE_ID,
    }
    return render(request, 'engineer_apply.html',context)


#engineer login
def engineer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('engineer_dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'engineer_login.html')

#enginer logout
def engineer_logout(request):
    logout(request)
    return render(request, 'engineer_logout.html')




#engineer account settings
@login_required
def engineer_settings(request):
    user = request.user
    
    # Get or create profile instance
    profile, created = EngineerProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile.phone = request.POST.get('phone', '')
        profile.Bio = request.POST.get('bio', '')
        profile.is_available = bool(request.POST.get('available'))
        profile.on_vacation = bool(request.POST.get('vacation'))
        profile.rating = request.POST.get('rating') or 0.0
       
        profile.is_available = 'is_available' in request.POST
        profile.on_vacation = 'on_vacation' in request.POST

        profile.surname = request.POST.get('surname')
        # profile.adress = request.POST.get('adress')
        profile.Specialization = request.POST.get('specialization')
        profile.profesional_summary = request.POST.get('professional_summary')
        

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            print("Uploaded:", profile.avatar.name)

        profile.save()
        return redirect('settings_engineer')  #  Redirect to same page or dashboard

    context = {
        'profile': profile
    }
    return render(request, 'engineer_setings.html', context)


#customer job posting
def post_job(request):
    return render(request, 'postJob.html')


#code sharing
def codeShare(request):
    profile, created = CodeShare.objects.get_or_create()
    if request.method == 'POST':
        profile.sharecode = request.POST.get('ShareCode')
        profile.save()
    context = {
        'profile': profile
    }
        
    return render(request, 'fileSharing.html', context)


#customer login
def customer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('customer_dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'customer_login.html')
 

def customer_logout(request):
    logout(request)
    return render(request, 'customer_logout.html')