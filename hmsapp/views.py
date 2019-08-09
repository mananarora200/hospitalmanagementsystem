from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from.forms import SignUpForm,UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def homepage(request):
    return render(request,'home.html')
    

def login_request(request):
    if request.method=='POST':
        form=UserLoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')  
            password= form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request,"login succesfully")
                return redirect('/')
            else:
                messages.error(request,"invalid username or password")
    else:
        form=UserLoginForm()
    return render(request,"login.html",context={'form':form})

def logout_request(request):
    logout(request)
    messages.info(request,"Logged out succesfully")
    return redirect('/login')
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.userprofile.gender = form.cleaned_data.get('gender')
            user.userprofile.city = form.cleaned_data.get('city')
            user.userprofile.birth_date = form.cleaned_data.get('birth_date')
            
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

                    


                 