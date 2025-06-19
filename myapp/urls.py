
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.engineer_signup, name='engineer_signup'),
    path('engineers/', views.engineer_directory, name='engineer_directory'),
    path('login/', views.engineer_login, name='engineer_login'),


  
  
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)