from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
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

class Case(models.Model):
    
    user = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    symptoms=models.CharField(max_length=60)
    disease=models.CharField(max_length=30, blank = True)
    starting_date=models.DateField(default=datetime.datetime.now())
    last_visit=models.DateField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.user.first_name)+"\t"+str(self.last_visit)

class Visits(models.Model):
    case_id=models.ForeignKey(Case,default=1,on_delete=models.CASCADE)
    medicine=models.CharField(max_length=50,blank=True)
    progress=models.CharField(max_length=20,blank=True)
    Date=models.DateField()
    test=models.CharField(max_length=50,blank=True)
    time=models.IntegerField()
    temperature=models.IntegerField()
    bp=models.IntegerField()
    symptoms=models.CharField(max_length=60)
    disease=models.CharField(max_length=30,blank=True)
    def __str__(self):
        return str(self.case_id)

class Medic(models.Model):
    
    visit_id=models.ForeignKey(Visits,on_delete=models.CASCADE)
    medicines=models.CharField(max_length=50)
    price=models.CharField(max_length=10)
    def __str__(self):
        return self.medicines

class Labs(models.Model):

    visit_id=models.ForeignKey(Visits,on_delete=models.CASCADE)
    test=models.CharField(max_length=50)
    price=models.CharField(max_length=10)
    def __str__(self):
        return self.test





