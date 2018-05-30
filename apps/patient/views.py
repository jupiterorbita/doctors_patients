from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.apps import apps
from django.contrib import messages
import bcrypt
doctors = apps.get_model('doctor', 'doctors')

# landing page
def home(request):
    print('\n   --> home.html <--')
    return render(request, 'patient/home.html')

def patient_landing(request):
    print('\n   --> patient_landing.html <--')
    return render(request, 'patient/patient_landing.html')

def index_html(request):
    print('\n   --> index html page <--')
    return render(request, 'patient/index.html')

def login_html(request):
    print('\n   --> login html <--')
    return render(request, 'patient/patient_login.html')

def register_html(request):
    doctor = doctors.objects.all()
    context = {
    'doctor':doctor
    }
    print('\n   --> register html <--')
    return render(request, 'patient/patient_register.html', context)

def registration_method(request):
    print('\n   --> registration method <--')
    if request.method == 'POST':
        errors = Patient.objects.registration_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/patient/register_html')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            Patient.objects.create(first_name=request.POST['first_name'], 
                                last_name=request.POST['last_name'], 
                                email=request.POST['email'], 
                                dob=request.POST['bday'], 
                                password=hashed_pw,
                                weight=request.POST['weight'],
                                height=request.POST['height'],
                                doctor_id=request.POST['doctor'],
                                address=request.POST['address'],
                                city=request.POST['city'],
                                state=request.POST['state'], 
                                zipcode=request.POST['zip'], 
                                phone=request.POST['phone'], 
                                diabetes=int(request.POST['diabetes']))
            request.session['patient_id'] = Patient.objects.get(email=request.POST['email']).id
            request.session['patient_first_name'] = Patient.objects.get(email=request.POST['email']).first_name
            request.session['patient_last_name'] = Patient.objects.get(email=request.POST['email']).last_name
            return redirect('/patient/dashboard_html')

def login_method(request):
    if request.method == 'POST':
        errors = Patient.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/patient/login_html')
        else:
            request.session['patient_id'] = Patient.objects.get(email=request.POST['email']).id
            return redirect('/patient/dashboard_html')

def dashboard_html(request):
    print('\n   --> dashboard <--')
    if 'patient_id' not in request.session:
        return redirect("/patient")
    else:
        patient = Patient.objects.get(id=request.session['patient_id'])
        doctor = doctors.objects.get(id=patient.doctor_id)
        data = entries.objects.filter(patient_id=request.session['patient_id']).order_by("-created_at")
        reventries = entries.objects.filter(patient_id=request.session['patient_id'])
        if patient.diabetes==0: 
             print("-"*50, "non diabetic")
             return render(request, 'patient/patient_dashboard_non-diabetic.html', {'doctor': doctor, 'patient':patient, "entries":data, "reventries":reventries})
        else:
            return render(request, 'patient/patient_dashboard.html', {'doctor': doctor, 'patient':patient, "entries":data, "reventries": reventries})


def that_info_html(request):
    print('\n   --> info <--')
    return render(request, 'patient/that_info.html')

def edit_profile_html(request):
    print('\n   --> info <--')
    patient = Patient.objects.get(id=request.session['patient_id'])
    return render(request, 'patient/edit_profile.html', {'patient': patient})



def logout(request):
    print("\n======> Server > Logout")
    request.session.clear()
    return redirect('/')

def about(request):
    print('\n ======> seerver > about')
    return render(request, 'patient/about.html')
def update_health(request):
    errors = Patient.objects.health_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/patient/dashboard_html')
    else:
        entries.objects.create(bloodsugar=request.POST['bloodsugar'],
                            systolic=request.POST['systolic'],
                            diastolic=request.POST['diastolic'],
                            heartrate=request.POST['heartrate'],
                            patient_id=request.session['patient_id']
                            )
        print("-"*50, "proccessing")
    return redirect('/patient/dashboard_html')