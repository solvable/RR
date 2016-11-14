from django import forms
from django.forms import SelectDateWidget, Textarea, EmailInput, HiddenInput
from .models import Customer, Jobsite, Appointment
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


class JobsiteForm(forms.ModelForm):

    class Meta:
        model = Jobsite
        fields = [
            "customer_id",
            "jobStreet",
            "jobCity",
            "jobState",
            "jobZip",
            "stories",
            "access",

            "notes",

            "latlng",
            "lat",
            "lng",

        ]
        widgets = {
            'notes': Textarea,
            'customer_id': HiddenInput,
            'latlng': HiddenInput,
            'lat':HiddenInput,
            'lng':HiddenInput,
        }
class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = [
            "jobsite_id",
            "title",
            "schedule_date",
            "time_slot",
            "problem",
            "assigned_to",
            "contract",
            "completed",
        ]
        widgets = {
            'schedule_date':SelectDateWidget,
            "jobsite_id":HiddenInput,
        }