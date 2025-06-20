# models.py

from django.contrib.auth.models import User
from django.db import models

class EngineerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='engineer_profile')
    phone = models.CharField(max_length=20)
    skills = models.TextField()
    is_available = models.BooleanField(default=True)
    on_vacation = models.BooleanField(default=False)
    rating = models.FloatField(default=0)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)

class ChatSession(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_chats')
    engineer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='engineer_chats')
    created = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    audio = models.FileField(upload_to='chat_audio/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Quotation(models.Model):
    engineer = models.ForeignKey(EngineerProfile, on_delete=models.CASCADE)
    chat = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    items = models.JSONField()  # List of dicts: [{material, qty, price}]
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending')
    reference = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

class EngineerScreening(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    email = models.EmailField()
    experience = models.TextField()
    project_type = models.TextField()
    tools = models.TextField()
    q1 = models.TextField()
    q2 = models.TextField()
    q3 = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.email
