from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    available_days = models.CharField(max_length=100)
    latitude = models.FloatField(default=20.5937)
    longitude = models.FloatField(default=78.9629)
    
    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"
    
#create models for user signup,login,etc 
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    mobile = models.BigIntegerField()
    password = models.CharField(max_length=50)


    def __str__(self):
        return self.name
