from django.contrib import admin

# Register your models here.
from .models import Customer, WorkOrder, Appointment

class CustomerAdmin(admin.ModelAdmin):
    list_display = ["lastName", "firstName", "billStreet", "billCity", "billState", "billZip", "phone1", "phone2", "email"]
    list_filter = ["modified"]
    search_fields=["lastName","billStreet"]
    class Meta:
        model = Customer

class JobsiteAdmin(admin.ModelAdmin):
    list_display = ["jobStreet","jobCity","jobState","jobZip","access","stories","notes","created","modified"]
    list_filter = ["modified"]
    search_fields=["jobStreet", "jobCity", "modified"]
    class Meta:
        model = WorkOrder

class AppointmentAdmin(admin.ModelAdmin):
    class Meta:
        model = Appointment



admin.site.register(Customer, CustomerAdmin)
admin.site.register(WorkOrder, JobsiteAdmin)
admin.site.register(Appointment, AppointmentAdmin)