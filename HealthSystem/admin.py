from django.contrib import admin

# Register your models here.
from .models import User, Comment, Appointment

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Appointment)