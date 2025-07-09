
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EngineerRegisterForm, CustomerRegisterForm
from .models import EngineerProfile, CustomerProfile,EngineerScreening,CodeShare,Job,ChatSession,Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import models

 

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




@login_required
def my_jobs_view(request):
    jobs = Job.objects.filter(customer=request.user).order_by('-created_at')  # Or use whatever timestamp field you have
    return render(request, 'customer_jobs.html', {'jobs': jobs})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, customer=request.user)
    if request.method == 'POST':
        job.delete()
        return JsonResponse({'deleted': True})

@login_required
def toggle_job_status(request, job_id):
    job = get_object_or_404(Job, id=job_id, customer=request.user)
    if request.method == 'POST':
        job.status = not job.status
        job.save()
        return JsonResponse({'status': job.status})
    

    
@login_required
def engineer_directory(request):
    engineers = EngineerProfile.objects.select_related('user').all()
    return render(request, 'engineers.html', {'engineers': engineers})


@login_required
def open_chat(request, engineer_id):
    engineer = get_object_or_404(User, pk=engineer_id)

    # Prevent user chatting with self
    if request.user == engineer:
        return redirect('somewhere_else')

    chat, created = ChatSession.objects.get_or_create(
        customer=request.user,
        engineer=engineer
    )

    messages = Message.objects.filter(chat=chat).order_by('timestamp')

    return render(request, 'chat_screen.html', {
        'chat': chat,
        'messages': messages,
        'engineer': engineer
    })

@login_required
def send_message(request, chat_id):
    chat = get_object_or_404(ChatSession, id=chat_id)
    if request.method == 'POST':
        content = request.POST.get('content', '')
        Message.objects.create(chat=chat, sender=request.user, content=content)
    return redirect('chat_screen', engineer_id=chat.engineer.id)



@login_required
def chat_inbox(request):
    user = request.user

    # Get all chat sessions where user is either customer or engineer
    chats = ChatSession.objects.filter(
        (models.Q(customer=user) | models.Q(engineer=user)),
        messages__isnull=False  # Only chats with at least one message
    ).distinct().select_related('customer', 'engineer').prefetch_related('messages')

    chat_data = []
    for chat in chats:
        last_message = chat.messages.last()
        other_user = chat.engineer if chat.customer == user else chat.customer
        profile = getattr(other_user, 'engineer_profile', None)
        chat_data.append({
            'chat': chat,
            'other_user': other_user,
            'profile': profile,
            'last_message': last_message,
        })

    return render(request, 'chat/chat_inbox.html', {'chats': chat_data})



@login_required
def engineer_chat_box(request):
    user = request.user
    sessions = ChatSession.objects.filter(engineer=user).order_by('-created')

    chat_list = []
    for session in sessions:
        # Get last message
        last_msg = session.messages.order_by('-timestamp').first()

        # Get customer profile if exists
        customer_profile = getattr(session.customer, 'customer_profile', None)

        chat_list.append({
            'other_user': session.customer,
            'profile': customer_profile,
            'last_message': last_msg
        })

    context = {
        'chats': chat_list
    }
    return render(request, 'engineer_chat/engineer_chat_box.html', context)


@login_required
def engineer_chat_screen(request, customer_id):
    user = request.user
    customer = get_object_or_404(User, id=customer_id)
    chat, created = ChatSession.objects.get_or_create(customer=customer, engineer=user)
    messages = chat.messages.order_by('timestamp')

    try:
        engineer_profile = user.engineer_profile
    except EngineerProfile.DoesNotExist:
        engineer_profile = None

    return render(request, 'engineer_chat/engineer_chat_screen.html', {
        'chat': chat,
        'messages': messages,
        'engineer_profile': engineer_profile,
        'customer': customer
    })

@login_required
def send_engineer_message(request, chat_id):

    
    chat = get_object_or_404(ChatSession, id=chat_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        latitude = request.POST.get('Latitude')
        longitude = request.POST.get('Longtitude')

        Message.objects.create(
            chat=chat,
            sender=request.user,
            content=content,
            Latitude=latitude if latitude else None,
            Longtitude=longitude if longitude else None
        )

        return redirect('engineer_chat_screen', customer_id=chat.customer.id)

    # If it's GET or anything else → just redirect back to chat screen
    return redirect('engineer_chat_screen', customer_id=chat.customer.id)




@login_required
def engineer_job_list(request):
    jobs = Job.objects.filter(status=True).order_by('-created_at')
    context = {'jobs': jobs}
    return render(request, 'engineer_job_list.html', context)



@login_required
def start_chat_with_customer(request, customer_id):
    customer = get_object_or_404(User, id=customer_id)

    # Check if chat already exists
    chat, created = ChatSession.objects.get_or_create(
        customer=customer,
        engineer=request.user
    )
    return redirect('engineer_chat_screen', customer_id=customer.id)
