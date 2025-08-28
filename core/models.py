from django.db import models
from django.utils import timezone


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # hashed password

    def __str__(self):
        return self.user_id


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.user_id}"


class LoginActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    login_user_id = models.CharField(max_length=50)  # attempted user_id
    login_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=(
        ('SUCCESS', 'SUCCESS'),
        ('FAILED', 'FAILED'),
    ))

    def __str__(self):
        return f"{self.login_user_id} - {self.status} at {self.login_time}"
