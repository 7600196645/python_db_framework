from django.db import models

# Create your models here.
<<<<<<< HEAD
class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name
    


=======
class User(models.Model):
    ROLE_CHOICES = [
        ('artist', 'Artist'),
        ('Customer', 'Customer'),
        ('admin', 'Admin'),
    ]
    username = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.BigIntegerField()
    password = models.CharField()
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='artist')
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)  # e.g., Singer, Painter
    rating = models.FloatField(default=0.0)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"
    
    def is_artist(self):
        return self.role == 'artist'
    
class PerformanceMedia(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performance_media')
    title = models.CharField(max_length=255)
    description = models.TextField()
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='uploads/media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_bookings')
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_by')
    status = models.CharField(max_length=20, choices=[('pending','Pending'),('confirmed','Confirmed'),('canceled','Canceled')], default='pending')
    booked_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.PositiveSmallIntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ArtistFeedback(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_given')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_received')
    rating = models.PositiveSmallIntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.artist.username} for {self.customer.username}"

class Feedback(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.customer}"
>>>>>>> 58fe60e7d81f7bfbd5bbf72179b00ddf9e542bfb
