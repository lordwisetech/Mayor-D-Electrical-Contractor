
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class EngineerManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None):
        if not email:
            raise ValueError('Engineers must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Engineer(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    skills = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='engineers/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = EngineerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin