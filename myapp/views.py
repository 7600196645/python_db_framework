from django.shortcuts import render,redirect,get_object_or_404
from .models import User,PerformanceMedia,Booking,ArtistFeedback,Review,Feedback
import random
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.utils import timezone
# Create your views here.
def dashboard(request):
    return render(request,'dashboard.html')

def admin_dashboard(request):
     if request.session.get("role") != "admin":
        return redirect("login")

     total_users = User.objects.exclude(role="admin").count()
     total_artists = User.objects.filter(role="artist").count()
     total_customers = User.objects.filter(role="customer").count()
     total_bookings = Booking.objects.count()
     pending_artists = User.objects.filter(role="artist", is_approved=False).count()
     total_reviews = Review.objects.count()
     total_feedbacks = Feedback.objects.count()

     stats = {
        "total_users": total_users,
        "total_artists": total_artists,
        "total_customers": total_customers,
        "total_bookings": total_bookings,
        "pending_artists": pending_artists,
        "total_reviews": total_reviews,
        "total_feedbacks": total_feedbacks,
    }
     return render(request, "admin_dashboard.html", {"stats": stats})
     
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            if user.password == password:
                # Store session values
                request.session['user_id'] = user.id
                request.session['email'] = user.email
                request.session['username'] = user.username
                request.session['role'] = user.role

                if user.role == "admin":
                    return redirect('dashboard')
                elif user.role == "customer":
                    return redirect('dashboard')  # customer dashboard
                elif user.role == "artist":
                    return redirect('dashboard')  # if exists
                else:
                    return redirect('login')  # fallback
            else:
                msg = 'Password does not match!'
                return render(request, 'login.html', {'msg': msg})
        except User.DoesNotExist:
            msg = "User does not exist!"
            return render(request, 'register.html', {'msg': msg})
    else:
        return render(request, 'login.html')

    
def register(request):
    if request.method =='POST':
        try:
            user = User.objects.get(email = request.POST['email'])
            msg = 'User already exists'
            return render(request,'register.html',{'msg' : msg})
        except:
            if request.POST['password'] == request.POST['confirm']:
                User.objects.create(
                    username = request.POST['username'],
                    email = request.POST['email'],
                    phone = request.POST['phone'],
                    password = request.POST['password'],
                    role = request.POST['role']
                    
                )
                msg = 'register Successfully!!!!'
                return render(request,'register.html',{'msg':msg})
            
            else:
                msg = 'Password & confirm password doesnot matched'
                return render(request,'register.html',{'msg':msg})
    else:
        return render(request,'register.html')
    
def logout_view(request):
    request.session.flush()  # Clears all session data
    return redirect('login')
 

def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "forget.html", {"msg": "Email not registered!"})

        # Generate and store OTP in session
        otp = str(random.randint(100000, 999999))
        request.session["email"] = email
        request.session["otp"] = otp

        # Send OTP (goes to console in development)
        send_mail(
            subject="Your OTP to reset password",
            message=f"Your OTP is: {otp}",
            from_email="nishapatel8399@gmail.com",  # Use dummy or test email
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect("otp")

    return render(request, "forget.html")


def otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        actual_otp = request.session.get("otp")

        if entered_otp == actual_otp:
            return redirect("reset_password")
        else:
            return render(request, "otp.html", {"msg": "Invalid OTP!"})

    return render(request, "otp.html")


def reset_password(request):
    if request.method == "POST":
        pwd1 = request.POST.get("new_password1")
        pwd2 = request.POST.get("new_password2")
        email = request.session.get("email")

        if pwd1 != pwd2:
            msg = "Passwords do not match"
            return render(request, "change_password.html", {"msg": msg})

        try:
            user = User.objects.get(email=email)
            user.password = pwd1  # or hash it later
            user.save()
            msg = "Password changed successfully!"
            request.session.pop("email", None)
            request.session.pop("otp", None)
            return redirect("login")
        except:
            msg = "Something went wrong"
            return render(request, "change_password.html", {"msg": msg})

    return render(request, "change_password.html")

def pd_change(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        email = request.session.get('email')  # Get current logged-in user's email

        try:
            user = User.objects.get(email=email)

            if user.password != old_password:
                msg = "Current password is incorrect."
                return render(request, 'password_change.html', {'msg': msg})

            if new_password1 != new_password2:
                msg = "New passwords do not match."
                return render(request, 'password_change.html', {'msg': msg})

            user.password = new_password1  # Optionally hash this
            user.save()
            msg = "Password updated successfully!"
            return render(request, 'password_change.html', {'msg': msg})

        except User.DoesNotExist:
            msg = "User not found."
            return render(request, 'password_change.html', {'msg': msg})

    return render(request, 'password_change.html')

def manage_profile(request):
    email = request.session.get("email")

    if not email:
        return redirect("login")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return redirect("login")

    if request.method == "POST":
        user.username = request.POST.get("name")
        user.phone = request.POST.get("phone")
        user.bio = request.POST.get("bio")  # Make sure 'bio' field exists in your User model
        
        user.save()
        msg = "Profile updated successfully!"
        return render(request, "manage_profile.html", {"user": user, "msg": msg})

    return render(request, "manage_profile.html", {"user": user})


def search_artist(request):
    artists = User.objects.filter(role='artist')

    for artist in artists:
        # Latest uploaded image (optional)
        artist.latest_image = (
            artist.performance_media
            .filter(media_type='image')
            .order_by('-uploaded_at')
            .first()
        )

        artist.media_titles = (
            artist.performance_media
            .values_list('title', flat=True)
            .distinct()
        )


    return render(request, 'search_artist.html', {'artists': artists})


def artist_profile(request, user_id):
    # Fetch the artist with the given ID and role
    artist = get_object_or_404(User, id=user_id, role='artist')

    # Get all uploaded media for that artist
    media_files = PerformanceMedia.objects.filter(user=artist)

    return render(request, 'artist_profile.html', {
        'artist': artist,
        'media_files': media_files
    })


def booking(request):
    return render(request,'booking.html')

def review(request):
    return render(request,'review.html')


def upload_media(request):
    # Get user info from session
    user_id = request.session.get('user_id')
    role = request.session.get('role')

    # Check if user is logged in and is an artist
    if not user_id or role != 'artist':
        messages.error(request, "Access denied. Only logged-in artists can upload media.")
        return redirect('login')

    # Get the artist user instance
    try:
        user = User.objects.get(id=user_id, role='artist')
    except User.DoesNotExist:
        messages.error(request, "Invalid artist user.")
        return redirect('login')

    # Handle POST form submission
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        media_type = request.POST.get('type')
        file = request.FILES.get('file')
        profile_image = request.FILES.get('profile_image')

        if title and description and media_type and file:
            # Save uploaded performance media
            PerformanceMedia.objects.create(
                user=user,
                title=title,
                description=description,
                media_type=media_type,
                file=file
            )

            # Update profile image if provided
            if profile_image:
                user.profile_image = profile_image
                user.save()

            messages.success(request, "Media uploaded successfully.")
            return redirect('upload_media')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'upload_media.html')

# Show book artist page
def bookings_page(request):
    if 'user_id' not in request.session or request.session['role'] != 'customer':
        return redirect('login')

    user_id = request.session['user_id']
    customer = get_object_or_404(User, id=user_id)

    # Fetch all artists
    artists = User.objects.filter(role='artist')

    # Attach latest media manually (as 'latest_media_title' attribute)
    for artist in artists:
        latest_media = PerformanceMedia.objects.filter(user=artist).order_by('-uploaded_at').first()
        artist.latest_media_title = latest_media.title if latest_media else None

    # Fetch this customer's bookings
    my_bookings = Booking.objects.filter(customer=customer).order_by('-booked_at')

    return render(request, 'book_artist.html', {
        'artists': artists,
        'my_bookings': my_bookings
    })


# Handle booking an artist
def book_artist(request, artist_id):
    if request.method == 'POST' and 'user_id' in request.session and request.session['role'] == 'customer':
        customer = get_object_or_404(User, id=request.session['user_id'])
        artist = get_object_or_404(User, id=artist_id, role='artist')

        # Optional: prevent double booking
        if Booking.objects.filter(customer=customer, artist=artist, status='pending').exists():
            return redirect('bookings')

        Booking.objects.create(
            customer=customer,
            artist=artist,
            status='pending',
            booked_at=timezone.now()
        )
    return redirect('bookings')


# Handle cancelling a booking
def cancel_booking(request, booking_id):
    if request.method == 'POST' and 'user_id' in request.session and request.session['role'] == 'customer':
        customer = get_object_or_404(User, id=request.session['user_id'])
        booking = get_object_or_404(Booking, id=booking_id, customer=customer)

        booking.status = 'canceled'
        booking.save()
    return redirect('bookings')


# View for artist to see bookings where they were booked
def artist_bookings(request):
    if 'user_id' not in request.session or request.session['role'] != 'artist':
        return redirect('login')

    artist = get_object_or_404(User, id=request.session['user_id'])
    bookings = Booking.objects.filter(artist=artist).order_by('-booked_at')

    return render(request, 'artist_book_can.html', {
        'bookings': bookings
    })


# Allow artist to cancel booking (shared cancel view)
def artcancel_booking(request, booking_id):
    if request.method == 'POST' and 'user_id' in request.session:
        user_id = request.session['user_id']
        role = request.session['role']

        booking = get_object_or_404(Booking, id=booking_id)

        # Allow cancel only if this user is either the customer or the artist involved
        if booking.customer.id == user_id or booking.artist.id == user_id:
            booking.status = 'canceled'
            booking.save()

        # Redirect based on user role
        if role == 'artist':
            return redirect('artist_bookings')
        else:
            return redirect('bookings')



def manage_booking(request):
    return render(request,'manage_booking.html')


def feedback_reviews(request):
    # Handle form submission (customer only)
    if request.method == 'POST' and request.session.get('role') == 'customer':
        user_id = request.session.get('user_id')
        artist_id = request.POST.get('artist_id')
        rating = request.POST.get('rating')
        content = request.POST.get('content')

        if artist_id and rating and content:
            Review.objects.create(
                customer_id=user_id,
                artist_id=artist_id,
                rating=int(rating),
                content=content,
                created_at=timezone.now()
            )
            messages.success(request, "Review submitted!")
            return redirect('feedback_reviews')
        else:
            messages.error(request, "All fields are required.")

    artists = User.objects.filter(role='artist')
    reviews = Review.objects.select_related('customer', 'artist').order_by('-created_at')
    
    return render(request, 'review.html', {
        'artists': artists,
        'reviews': reviews
    })



from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import User, ArtistFeedback

def feedback_by_artist_list(request):
    artist_id = request.session.get('user_id')
    role = request.session.get('role')

    if not artist_id or role != 'artist':
        messages.error(request, "Access denied.")
        return redirect('login')

    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        rating = request.POST.get('rating')
        content = request.POST.get('content')

        if customer_id and rating and content:
            exists = ArtistFeedback.objects.filter(
                artist_id=artist_id,
                customer_id=customer_id
            ).exists()

            if exists:
                messages.error(request, "You already submitted feedback for this customer.")
            else:
                ArtistFeedback.objects.create(
                    artist_id=artist_id,
                    customer_id=customer_id,
                    rating=int(rating),
                    content=content,
                    created_at=timezone.now()
                )
                messages.success(request, "Feedback submitted successfully.")
                return redirect('feedback_by_artist_list')
        else:
            messages.error(request, "All fields are required.")

    customers = User.objects.filter(role='Customer')
    feedbacks = ArtistFeedback.objects.filter(artist_id=artist_id).select_related('customer').order_by('-created_at')

    return render(request, 'feedbackcus.html', {
        'customers': customers,
        'feedbacks': feedbacks
    })


def add_artist(request):
    return render(request,'add_artist.html')

def manage_users(request):
    if request.session.get('role') != 'admin':
        messages.error(request, "Access denied.")
        return redirect('login')

    users = User.objects.exclude(role='admin')  # Show only customers and artists
    return render(request, 'manage_artist_customer.html', {'users': users})

def admin_view_user(request, user_id):
    if request.session.get('role') != 'admin':
        messages.error(request, "Access denied.")
        return redirect('login')
    user_obj = get_object_or_404(User, id=user_id)
    return render(request, 'admin-view_user.html', {'user_obj': user_obj})

def admin_edit_user(request, user_id):
    if request.session.get('role') != 'admin':
        messages.error(request, "Access denied.")
        return redirect('login')
    user_obj = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user_obj.username = request.POST.get('username')
        user_obj.email = request.POST.get('email')
        user_obj.phone = request.POST.get('phone')
        user_obj.role = request.POST.get('role')
        user_obj.category = request.POST.get('category', user_obj.category)
        user_obj.bio = request.POST.get('bio', user_obj.bio)
        if 'profile_image' in request.FILES:
            user_obj.profile_image = request.FILES['profile_image']
        user_obj.save()
        messages.success(request, "User updated successfully.")
        return redirect('admin_manage_users')

    return render(request, 'admin_edit_user.html', {'user_obj': user_obj})

def admin_delete_user(request, user_id):
    if request.session.get('role') != 'admin':
        messages.error(request, "Access denied.")
        return redirect('login')
    user_obj = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('admin_manage_users')

    return render(request, 'admin-delete_user.html', {'user_obj': user_obj})

def view_all_bookings(request):
    # fetch all bookings
    if request.session.get("role") != "admin":
        return redirect("login")
    bookings = Booking.objects.all()
    return render(request, "view_all_bookings.html", {"bookings": bookings})
    

def view_all_reviews(request):
    # fetch all reviews
    if request.session.get("role") != "admin":
        return redirect("login")
    reviews = Review.objects.all()
    return render(request, "view_all_reviews.html", {"reviews": reviews})

    
def approve_artist(request):
    # approve pending artist accounts
    if request.session.get("role") != "admin":
        return redirect("login")
    artist_id = request.GET.get("id")
    if artist_id:
        artist = get_object_or_404(User, id=artist_id, role="artist")
        artist.is_approved = True
        artist.save()
        messages.success(request, f"Artist {artist.username} approved successfully!")
        return redirect("approve_artist")

    pending_artists = User.objects.filter(role="artist", is_approved=False)
    return render(request, "approve_artist.html", {"pending_artists": pending_artists})
    
def view_all_feedbacks(request):
    # fetch all feedbacks
    if request.session.get("role") != "admin":
        return redirect("login")
    feedbacks = Feedback.objects.all()
    return render(request, "view_all_feedbacks.html", {"feedbacks": feedbacks})
 
