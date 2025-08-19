from django.contrib import admin
<<<<<<< HEAD
from . models import *

# Register your models here.
admin.site.register(Patient)
=======
from .models import User,PerformanceMedia,Booking,ArtistFeedback,Review
# Register your models here.

admin.site.register(User)
admin.site.register(PerformanceMedia)
admin.site.register(Booking)
admin.site.register(ArtistFeedback)
admin.site.register(Review)
>>>>>>> 58fe60e7d81f7bfbd5bbf72179b00ddf9e542bfb
