from django.contrib import admin

# Register your models here.
from .models import Doctor, Appointment

from django.contrib import admin
from .models import Doctor, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('title', 'first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'time')
    search_fields = ('doctor__first_name', 'doctor__last_name', 'patient__first_name', 'patient__last_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_patient:
            return qs.filter(patient=request.user.patient)
        return qs

admin.site.register(Appointment, AppointmentAdmin)
