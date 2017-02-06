from django.contrib import admin

# Register your models here.
from thoughts.models import bella, UserProfile
admin.site.register(bella)
admin.site.register(UserProfile)