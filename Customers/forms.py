from django import forms
from django.forms import SelectDateWidget, Textarea, EmailInput, HiddenInput
from .models import Customer, WorkOrder, Appointment
from haystack.forms import SearchForm


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "firstName",
            "lastName",
            "billStreet",
            "billCity",
            "billState",
            "billZip",
            "phone1",
            "phone2",
            "email",
            "source"
        ]
        widgets = {'email':EmailInput}


class WorkOrderForm(forms.ModelForm):

    class Meta:
        model = WorkOrder
        fields = [
            "customer_id",
            "jobStreet",
            "jobCity",
            "jobState",
            "jobZip",
            "stories",
            "access",
            "problem",
            "notes",
            "assigned_to",
            "crew_assigned",
            "contract",
            "completed",
            "latlng",
            "lat",
            "lng",

        ]
        widgets = {
                   'notes': Textarea,
                   'customer_id': HiddenInput,
                   }
class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = [
            "workorder_id",
            "title",
            "schedule_date",
            "time_slot"
        ]
        widgets = {
            'schedule_date':SelectDateWidget,
            'workorder_id':HiddenInput,
        }