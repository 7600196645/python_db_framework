from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from . models import Doctor,Profile,User,Patient
# Register your models here.

#15) Write a Django project that customizes the admin panel to display more detailed doctor information (e.g., specialties, availability).
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):                    #
    list_display=('name','specialization','phone','email','available_days')
    search_fields =('name','specialization','email')
    list_filter = ('specialization','available_days')

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Unregister the original User admin
admin.site.unregister(User)

# Register the new User admin
admin.site.register(User, UserAdmin)

# Optionally register Profile directly too
admin.site.register(Profile)
