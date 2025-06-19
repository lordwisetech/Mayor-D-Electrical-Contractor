
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
  
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)