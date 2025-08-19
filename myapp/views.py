from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')

def profile(request):
    doctor = {
        'name': 'Dr. Emily Carter',
        'specialization': 'Cardiologist',
        'location': 'New York, NY',
        'email': 'emily.carter@example.com'
    }
    return render(request,'profile.html',{'doctor':doctor})

def contact(request):
    return render(request,'contact.html')

def patient_form(request):
    return render(request,'patient_form.html')

