from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    city=models.CharField(max_length=10)
    gender=models.CharField(max_length=10)
    role=models.CharField(max_length=10,default='patient')
    birth_date = models.DateField(null=True, blank=True)

    
    def __str__(self):
        return "{0} {1}" .format(self.user.first_name,self.user.last_name)    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

