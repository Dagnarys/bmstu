from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Insurance)
admin.site.register(Driver)
admin.site.register(CustomUser)
