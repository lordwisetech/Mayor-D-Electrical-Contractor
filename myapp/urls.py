
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/engineer/', views.register_engineer, name='register_engineer'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('account/engineer/', views.engineer_dash, name='engineer_dashboard'),
    path('account/', views.customer_dash, name='customer_dashboard'),
    path('engineer/apply/', views.engineer_apply, name='engineer_apply'),
    path('engineer/apply/save/', views.save_screening_data, name='save_engineer_data'),
    path('login/engineer/', views.engineer_login, name='engineer_login'),
   path('logout/engin', views.engineer_logout, name='engineer_logout'),
   path('account/settings/', views.engineer_settings, name='settings_engineer'),
   
   path('customer/login/', views.customer_login, name='customer_login'),
   path('logout/',views.customer_logout, name='logout'),


   path('code/', views.codeShare, name='codeshare'),
   path('myjobs/', views.my_jobs_view, name='myjob'),
   path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
   path('toggle-job-status/<int:job_id>/', views.toggle_job_status, name='toggle_job_status'),
   path('engineers/', views.engineer_directory, name='engineer_directory'),
   path('chat/<int:engineer_id>/', views.open_chat, name='chat_screen'),
   path('chat/<int:chat_id>/send/', views.send_message, name='send_message'),
   path('inbox/', views.chat_inbox, name='chat_inbox'),


    path('engineer/chats/', views.engineer_chat_box, name='engineer_chat_box'),
    path('engineer/chat/<int:customer_id>/', views.engineer_chat_screen, name='engineer_chat_screen'),
    path('engineer/send/<int:chat_id>/', views.send_engineer_message, name='send_engineer_message'),

    path('engineer/jobs/', views.engineer_job_list, name='engineer_job_list'),
    path('engineer/start_chat/<int:customer_id>/', views.start_chat_with_customer, name='start_chat_with_customer'),

  
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

