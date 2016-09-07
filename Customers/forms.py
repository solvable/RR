from django import forms

from .models import Customer, WorkOrder
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
            "schedule_date",
            "assigned_to",
            "crew_assigned",
            "contract",
            "completed",
            "latlng",
            "lat",
            "lng",

        ]

