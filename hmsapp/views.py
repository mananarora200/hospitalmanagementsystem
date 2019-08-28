from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import SignUpForm,UserLoginForm, HistoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import UserProfile, UserHistory,Labs,Medic
# Create your views here.
@login_required
def homepage(request):
    return render(request,'home.html')
    
@login_required
def showpatienthistory(request):
    data = UserHistory.objects.get(user = request.user)
    args = {"diabetes":data.diabetes,
    "bp":data.blood_pressure,
    "hp":data.heart_problems,
    "drink":data.drink,
    "smoke":data.smoke,
    "drugs":data.drugs}
    return render(request,"patienthistory.html", context=args)

def login_request(request):
    if request.method=='POST':
        form=UserLoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')  
            password= form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                data = UserProfile.objects.get(user = request.user)
                if data.history_completed == False:
                    return redirect("/patienthistory")
                else:
                    return redirect("/")
            else:
                messages.error(request,"Invalid Username or Password")
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
            user.refresh_from_db()
            user.userprofile.gender = form.cleaned_data.get('gender')
            user.userprofile.city = form.cleaned_data.get('city')
            user.userprofile.birth_date = form.cleaned_data.get('birth_date')
            
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('patienthistory')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
@login_required
def userhistory(request):
    if request.method == "POST":
        form = HistoryForm(request.POST)
        if form.is_valid():
            current_history = form.save(commit=False)
            current_history.user = request.user
            current_history.save()
            data = UserProfile.objects.get(user = request.user)
            data.history_completed = True
            data.save()
            return HttpResponseRedirect('/')
    else:
        form = HistoryForm()
    return render(request,'history.html',context={'form':form})                    
def medicine(request):
    all_objects=Medic.objects.all()

    context= {'all_objects':all_objects}

    return render(request,'medicine.html',context)
def test(request):
    all_objects=Labs.objects.all()

    context= {'all_objects':all_objects}

    return render(request,'lab.html',context)

                 
