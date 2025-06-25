
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
   path('post*#job/', views.post_job, name='post_job'),
   path('customer/login/', views.customer_login, name='customer_login'),
   path('logout/',views.customer_logout, name='logout'),


   path('code/', views.codeShare, name='codeshare'),

  
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

