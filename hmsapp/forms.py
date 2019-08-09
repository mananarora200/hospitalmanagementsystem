from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
CHOICES= [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
    
    ]
class UserLoginForm(forms.Form):
     username=forms.CharField(max_length=20,label='phone no')
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


