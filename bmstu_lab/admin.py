from django.contrib import admin

# Register your models here.
from .models import Insurance, DriverInsurance, Driver, Users

admin.site.register(Insurance)
admin.site.register(DriverInsurance)
admin.site.register(Driver)
admin.site.register(Users)
