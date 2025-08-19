from django.contrib import admin
from .models import User,PerformanceMedia,Booking,ArtistFeedback,Review
# Register your models here.

admin.site.register(User)
admin.site.register(PerformanceMedia)
admin.site.register(Booking)
admin.site.register(ArtistFeedback)
admin.site.register(Review)
