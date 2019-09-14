from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import SignUpForm,UserLoginForm, HistoryForm,CreateCase,CreateVisit
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import UserProfile, UserHistory,Labs,Medic, User,Case,Visits,Current


@login_required
def homepage(request):
    data = UserProfile.objects.get(user = request.user)
    if data.role == "patient":
        return render(request,'patienthome.html')
    elif data.role == "doctor":
        data = Current.objects.get(id = 1)
        current_doc = data.cdoc
        data_visit = Visits.objects.get(id = current_doc)
        data_case = Case.objects.get(id = data_visit.case_id)
        data_patient = User.objects.get(id = data_case.user_id)
        patient_profile = UserProfile.objects.get(user = data_case.user)
        patient_history = UserHistory.objects.get(user = data_case.user)
        context = {
            "profile":patient_profile,
            "history":patient_history,
            "visit":data_visit,
            "patient":data_patient,
            "case":data_case,
        }
        current_doc = current_doc + 1
        data.cdoc = current_doc
        data.save()
        return render(request, "doctorhome.html", context)  

    elif data.role == "medic":
        return render(request, "medic.html")
    elif data.role == "lab":
        return render(request, "lab.html") 
    elif data.role == "mediocar":
        return render(request, "mediocarhome.html")        
    

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


@login_required
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


@login_required                    
def medicine(request):
    
    data=Current.objects.get(id=1)
    current_medic=data.cmedic
    data_new=Medic.objects.get(id=current_medic)
    context= {'medicine':data_new.medicines.split('\n'),
    }
    current_medic=current_medic+1
    data.cmedic=current_medic
    data.save()
    return render(request,'medicine.html',context)
    
          
@login_required    
def test(request):
    i=1
    data=Current.objects.get(id=1)

    current_lab=data.clab
    data_new=Labs.objects.get(id=current_lab)
    

    context= {'lab':data_new.test.split('\n'),
    'i':i
    
    }
    current_lab=current_lab+1
    data.clab=current_lab
    data.save()
    return render(request,'lab.html',context)

@login_required
def showpatientprofile(request):
    dataprofile = UserProfile.objects.get(user = request.user)
    datauser = User.objects.get(id = request.user.id)
    args = {
        "name":datauser.first_name +" "+ datauser.last_name,
        "phone":datauser.username,
        "email":datauser.email,
        "birthdate":dataprofile.birth_date,
        "gender":dataprofile.gender,
        "city":dataprofile.city
    }
    return render(request, "userprofile.html", context=args)

@login_required
def createcase(request):
    if request.method == "POST":
        form = CreateCase(request.POST)
        if form.is_valid():
            current_case = form.save(commit=False)
            current_case.user = request.user
            current_case.save()
            current_visit = Visits.objects.create(current_status = current_case.symptoms, time = request.POST.get("time"), case_id = current_case.id)
            current_visit.save()
            return redirect("/")
    else:
        form = CreateCase()
    return render(request,'createcase.html',context={'form':form})

@login_required
def existingcase(request):
    data=Case.objects.filter(user = request.user)
    case_list = []
    for cases in data:
        one_case = (cases.symptoms+" "+str(cases.starting_date), cases.id)
        case_list.append(one_case)
    if request.method == "POST":
        form = CreateVisit(request.POST)
        if form.is_valid():
            current_visit = form.save(commit= False)
            print(current_visit.time)
            cname=request.POST.get('dropdown1')
            current_visit.case_id=cname
            current_visit.save()
            return HttpResponseRedirect('/')
    else:
        form = CreateVisit()
    context = {
        "form":form,
        "cases":data,
    }
    return render(request,'createvisit.html',context=context)

@login_required
def save_medic(request):
    data=Current.objects.get(id=1)
    price=request.POST.get('price')
    current_medic=data.cmedic
    data_new=Medic.objects.get(id=current_medic-1)
    data_new.price=price
    data_new.save()
    return render(request,'save_medic.html')

@login_required
def save_lab(request):
    data=Current.objects.get(id=1)
    price1=request.POST.get('price1')
    current_lab=data.clab
    data_new=Labs.objects.get(id=current_lab-1)
    data_new.price=price1
    data_new.save()
    return render(request,'save_lab.html')


@login_required        
def mediocar(request):
    data=Current.objects.get(id=1)
    current_visit=data.cvisit
    data_new=Visits.objects.get(id=current_visit)
    context= {'case':data_new.case,
    }
    current_visit=current_visit+1
    data.cvisit=current_visit
    data.save()
    return render(request,'mediocar.html',context)

@login_required    
def save_mediocar(request):
    data=Current.objects.get(id=1)
    temperature=request.POST.get('temperature')
    bp=request.POST.get('bp')
    current_visit=data.cvisit
    data_new=Visits.objects.get(id=current_visit-1)
    data_new.temperature=temperature
    data_new.bp=bp
    data_new.save()
    return render(request,'save_mediocar.html')   
 
@login_required
def save_doc(request):
    data=Current.objects.get(id=1)
    disease=request.POST.get('disease')
    medicines=request.POST.get('medicines')
    test=request.POST.get('test')
    current_visit=data.cdoc
    data_new=Visits.objects.get(id=current_visit-1)
    data_new1=Medic.objects.create(medicines = medicines, visit_id = current_visit-1)
    data_new2=Labs.objects.create(test = test, visit_id = current_visit-1)
    data_new.disease=disease
    data_new.save()
    data_new1.save()
    data_new2.save()
    return render(request,'save_doc.html')

        


