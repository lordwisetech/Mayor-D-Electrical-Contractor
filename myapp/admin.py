from django.contrib import admin
from .models import  CustomerProfile, EngineerProfile,ChatSession, Message, Quotation, Payment, Notification,EngineerScreening
# Register your models here.
admin.site.register(CustomerProfile)
admin.site.register(EngineerProfile)
admin.site.register(ChatSession)
admin.site.register(Message)
admin.site.register(Quotation)
admin.site.register(Payment)
admin.site.register(Notification)
admin.site.register(EngineerScreening)