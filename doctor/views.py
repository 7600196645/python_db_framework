
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,update_session_auth_hash,logout as auth_logout
from django.contrib import messages
from . models import Doctor,Profile,User
from . forms import SignupForm,UpdateProfileForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
import json


# Create your views here.

MERCHANT_KEY = 'your_merchant_key'
MERCHANT_ID = 'your_mid'
PAYTM_URL = 'https://securegw-stage.paytm.in/order/process'  # use live URL for production


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('profile')
        
    else:
        form = SignupForm()
    return render(request,'signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)   #django automatically bind request data to the form
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)   #Django checks if a user exists with the given username and password.
            if user is not None:
                login(request, user)     #django create session  and user stay logged in page
                messages.success(request, f"Welcome {username}!")
                return redirect('profile')  # Redirect to your homepage or dashboard
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
        
# Logout View
@login_required
def logout(request):
    auth_logout(request)  # This clears the session
    return redirect('login_view')  # Redirect to login page after logout

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

# Password Change View
@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important! Keeps the user logged in after password change
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password_change.html', {'form': form})

# Password Change Done View
@login_required
def pass_change_done(request):
    return render(request, 'pass_change_done.html')

def doctor_info(request):
      doctors = Doctor.objects.all()
      return render(request,'doctor_info.html',{'doctors':doctors})  

def doctor_profile(request):
    
    if request.method == 'POST':
        name = request.POST['name']
        specialization = request.POST['specialization']
        email = request.POST['email']
        phone = request.POST['phone']
        available_days = request.POST['available_days']

        doctor = Doctor(
            name=name,
            specialization=specialization,
            email=email,
            phone=phone,
            available_days=available_days
        )
        
        doctor.save()
        msg = 'Doctor info add successfully'
        return render(request, 'doctor_profile.html',{'msg' : msg})  # Or redirect to a success page

    else:
        return render(request, 'doctor_profile.html')
    
def doctor_update(request,pk):
    doctor = get_object_or_404(Doctor,pk=pk)
    if request.method == "POST":
        doctor.name = request.POST.get('name')
        doctor.specialization = request.POST.get('specialization')
        doctor.email = request.POST.get('email')
        doctor.phone = request.POST.get('phone')
        doctor.available_days = request.POST.get('available_days')
       
        doctor.save()
        
        return redirect('doctor_info')
    else:
          return render(request,'doc_profile_update.html',{'doctor':doctor})  
    
def doctor_delete(request,pk):
    doctor = get_object_or_404(Doctor,pk=pk)
    if request.method =='POST':
        doctor.delete()
        return redirect('doctor_info')
    return render(request,'doctor_delete.html',{'doctor':doctor})
    
def index(request):
    doctors = Doctor.objects.all()
    return render(request, 'index.html', {'doctors': doctors})

def add_doctor(request):
    if request.method == 'POST':
        name = request.POST['name']
        specialization = request.POST['specialization']
        email = request.POST['email']
        phone = request.POST['phone']
        available_days = request.POST['available_days']
        doctor = Doctor.objects.create(name=name, specialization=specialization, email=email, phone=phone, available_days=available_days)
        return JsonResponse({'id': doctor.id, 'name': doctor.name, 'specialization': doctor.specialization, 'email': doctor.email, 'phone': doctor.phone, 'available_days' : doctor.available_days})

def delete_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    doctor.delete()
    return JsonResponse({'status': 'deleted'})

def update_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    if request.method == 'POST':
        doctor.name = request.POST['name']
        doctor.specialization = request.POST['specialization']
        doctor.email = request.POST['email']
        doctor.phone = request.POST['phone']
        doctor.available_days = request.POST['available_days']
        doctor.save()
        return JsonResponse({'id': doctor.id, 'name': doctor.name, 'specialization': doctor.specialization, 'email': doctor.email, 'phone': doctor.phone , 'available_days' : doctor.available_days})


def appoinment(request):  # Consider renaming to `razorpay_payment` for clarity
    doctors = Doctor.objects.all()  # fetch all doctors
    amount = 5000  # Amount in paise (₹500)

    # Razorpay client instance
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay Order
    payment = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': '1',  # Auto capture after payment
    })

    # Pass everything to the template
    context = {
        'doctors': doctors,
        'payment': payment,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
    }

    return render(request, 'appoinment.html', context)
    
    

def payment_success(request):
    return render(request,'success.html')       

def doctor_map(request):
    doctors = Doctor.objects.all()
    doctor_data = [
        {
            'name': doc.name,
            'specialization': doc.specialization,
            'latitude': doc.latitude,
            'longitude': doc.longitude,
            'address': doc.address if hasattr(doc, 'address') else ''
        }
        for doc in doctors
    ]
    return render(request, 'map.html', {'doctors': json.dumps(doctor_data)})
       