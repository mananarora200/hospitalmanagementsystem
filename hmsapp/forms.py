from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import UserHistory,Case,Visits
CHOICES= [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
    
    ]

class UserLoginForm(forms.Form):
     username=forms.CharField(max_length=20,label='Phone Number')
     password=forms.CharField(max_length=100,widget=forms.PasswordInput)
      
           

class SignUpForm(UserCreationForm):
    
    gender=forms.CharField(max_length=10,label='gender', widget=forms.RadioSelect(choices=CHOICES))
    city=forms.CharField(max_length=10)
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    email =forms.EmailField(required=True)
    first_name=forms.CharField(max_length=20)
    last_name=forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['first_name','last_name','username','birth_date', 'password1', 'password2','gender','city','email' ]


class HistoryForm(forms.ModelForm):
    choices1 = [
    ('Never', 'Never'),
    ('Once an year', 'Once an year'),
    ('Few times a year', 'Few times a year'),
    ('Few times a month', 'Few times a month'),
    ('Few times a week', 'Few times a week'),
    ('Daily', 'daily'),
    ('Many times a day', 'Many times a day'),    
    ]
    choices2 = [
    ('Yes', 'Yes'),
    ('No', 'No'),
    ]
    diabetes=forms.CharField(max_length=100,label='Do you have Diabetes?', widget=forms.RadioSelect(choices=choices2))
    blood_pressure=forms.CharField(max_length=100,label='Do you have Blood Pressure Problems?', widget=forms.RadioSelect(choices=choices2))
    heart_problems=forms.CharField(max_length=100,label='Do you have have Heart Problems?', widget=forms.RadioSelect(choices=choices2))
    drink=forms.CharField(max_length=100,label='How often do you have alcohol?', widget=forms.RadioSelect(choices=choices1))
    smoke=forms.CharField(max_length=100,label='How often do you smoke?', widget=forms.RadioSelect(choices=choices1))
    drugs=forms.CharField(max_length=100,label='How often do you have drugs?', widget=forms.RadioSelect(choices=choices1))
    class Meta:
        model = UserHistory
        fields = ["diabetes",
        "blood_pressure",
        "heart_problems",
        "drink",
        "smoke",
        "drugs",]

class CreateCase(ModelForm):
    class Meta:
        model = Case
        fields = ['symptoms',]

class CreateVisit(ModelForm):
    class Meta:
        model = Visits
        fields = ["current_status","time"]