from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from .models import (
    CustomerProfile, EngineerProfile, ChatSession, Message,
    Quotation, Payment, Notification, EngineerScreening
)

# Register your other models
admin.site.register(CustomerProfile)
admin.site.register(EngineerProfile)
admin.site.register(ChatSession)
admin.site.register(Message)
admin.site.register(Quotation)
admin.site.register(Payment)
admin.site.register(Notification)

# Define Accept action
@admin.action(description="Accept Engineer")
def accept_engineer(modeladmin, request, queryset):
    for obj in queryset:
        send_mail(
            "🎉 You're Accepted – Mayor D Electrical Contractor",
            f"""
Dear Engineer,

Congratulations! You have been accepted to register on the Mayor D Electrical Contractor platform.

Please proceed to complete your registration here:
https://mayor-d-electrical-contractor.onrender.com/register/engineer

Welcome aboard!

– Mayor D Team
""",
            settings.DEFAULT_FROM_EMAIL,
            [obj.email],
            fail_silently=False,
        )

# Define Reject action
@admin.action(description="❌ Reject Engineer")
def reject_engineer(modeladmin, request, queryset):
    for obj in queryset:
        send_mail(
            "Application Status – Mayor D Electrical Contractor",
            f"""
Dear Applicant,

We appreciate your interest in working with Mayor D Electrical Contractor.

Unfortunately, after reviewing your application, we will not be proceeding further at this time.

We wish you all the best in your future endeavors.

– Mayor D Team
""",
            settings.DEFAULT_FROM_EMAIL,
            [obj.email],
            fail_silently=False,
        )

# Register EngineerScreening with actions
@admin.register(EngineerScreening)
class EngineerScreeningAdmin(admin.ModelAdmin):
    list_display = ('email', 'experience', 'submitted_at')
    actions = [accept_engineer, reject_engineer]


admin.site.site_header = "Mayor D Electrical Contractor Admin"
admin.site.site_title = "Mayor D Control Panel"
admin.site.index_title = "Welcome to Mayor D Electrical Contractor Admin"
# Ensure the admin interface is user-friendly
