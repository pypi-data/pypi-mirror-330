# models.py
from django.db import models
from django.contrib.auth.models import User

class ThemeSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=50, choices=[
        ('default', 'Default'),
        ('blue', 'Blue Theme'),
        ('green', 'Green Theme'),
        ('dark', 'Dark Mode'),
    ], default='default')
    
    def __str__(self):
        return f"{self.user.username} - {self.theme}"
