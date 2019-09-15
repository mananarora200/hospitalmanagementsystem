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

class Case(models.Model):
    user = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    symptoms=models.CharField(max_length=60)
    disease=models.CharField(max_length=30, blank = True)
    starting_date=models.DateField(auto_now= True)
    last_visit=models.DateField(blank = True, null = True)
    def __str__(self):
        return str(self.user.first_name)+"\t"+str(self.last_visit)

class Visits(models.Model):
    case = models.ForeignKey(Case,default=1,on_delete=models.CASCADE)
    progress = models.CharField(max_length=50,blank=True)
    date = models.DateField(auto_now = True)
    temperature = models.IntegerField(blank = True, null  = True)
    bp = models.CharField(max_length = 6, blank = True)
    current_status = models.CharField(max_length=60)
    disease = models.CharField(max_length=30,blank=True)
    time = models.TimeField(default = "00:00")
    def __str__(self):
        return str(self.case_id)

class Medic(models.Model):
    visit=models.ForeignKey(Visits,on_delete=models.CASCADE)
    medicines=models.TextField(max_length=100)
    price=models.TextField(max_length=10)
    def __str__(self):
        return self.medicines

class Labs(models.Model):
    visit=models.ForeignKey(Visits,on_delete=models.CASCADE)
    test=models.TextField(max_length=50)
    price=models.TextField(max_length=10)
    def __str__(self):
        return self.test
    
class Current(models.Model):
    cmedic=models.IntegerField()
    clab=models.IntegerField()
    cdoc = models.IntegerField(default = 1)
    cvisit = models.IntegerField(default = 1)
    






