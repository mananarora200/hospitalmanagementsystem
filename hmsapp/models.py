from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    city=models.CharField(max_length=10)
    gender=models.CharField(max_length=10)
    role = models.CharField(max_length=10,default='patient')
    birth_date = models.DateField(null=True, blank=True)
    history_completed = models.BooleanField(default=False)

    
    def __str__(self):
        return "{0} {1}" .format(self.user.first_name,self.user.last_name)    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

class UserHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    diabetes = models.CharField(max_length = 100)
    blood_pressure = models.CharField(max_length = 100)
    heart_problems = models.CharField(max_length = 100)
    drink = models.CharField(max_length = 100)
    smoke = models.CharField(max_length = 100)
    drugs = models.CharField(max_length = 100)
    def __str__(self):
        return "{0} {1}" .format(self.user.first_name,self.user.last_name)
