from django.contrib import admin
from account.models import User, Appointment, VaccineStatus, Vaccine

# Register your models here.

admin.site.register(User)
admin.site.register(VaccineStatus)
admin.site.register(Vaccine)

admin.site.register(Appointment)