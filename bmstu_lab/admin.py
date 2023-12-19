from django.contrib import admin

# Register your models here.
from .models import Insurance, Driver, Users

admin.site.register(Insurance)
admin.site.register(Driver)
admin.site.register(Users)
