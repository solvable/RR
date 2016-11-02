import re
import haystack as haystack
import whoosh
import datetime
from forecastio import load_forecast
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from .models import Customer, WorkOrder
from .forms import CustomerForm, WorkOrderForm
from django import forms
from schedule.models import Event, EventRelation, Calendar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from haystack.management.commands import update_index, rebuild_index
from schedule.models import Event, Calendar
import simplejson
from django.core import serializers


def search(request):
    return HttpResponse(fuckoff)

def index(request):
    import pyowm
    API_KEY = '0661037c3beedfccf03d405e5ed322e4'
    LOCATION_ID = 5205788
    owm=pyowm.OWM(API_KEY)


    observation = owm.weather_at_id(LOCATION_ID)
    w = observation.get_weather()

    status = w.get_detailed_status()
    weather_icon = w.get_weather_icon_name()
    icon = "http://openweathermap.org/img/w/"+weather_icon+".png"

    temp = w.get_temperature('fahrenheit')
    temp_max = temp["temp_max"]
    temp_min = temp["temp_min"]

    wind = w.get_wind()
    wind_speed = wind["speed"]

    fc = owm.daily_forecast_at_id(LOCATION_ID, limit=5)
    f = fc.get_forecast()
    lst = f.get_weathers()







    context = {
        "title":"Home",
        "status": status,
        "icon":icon,
        "wind_speed":wind_speed,
        "temp_max":temp_max,
        "temp_min":temp_min,
        "f":f,
        "lst":lst,

    }
    return render(request, "index.html", context)




def customer_list(request):
    """
    View for customer list
    :param request:
    :return: list of all customer objects rendered on 'customer_list.html'
    """
    queryset_list = Customer.objects.all()
    paginator = Paginator(queryset_list, 2) # show 15 customers per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer deliver first page
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        queryset = paginator.page(paginator.num_pages)

    # Set context variables
    context = {
            "title":"Recent Customers",
            "object_list": queryset,
            "page_request_var":page_request_var,
        }
    return render(request, "customer_list.html", context)


def customer_create(request):
    '''
    View to create a Customer object
    '''
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404


    # Load Customer Form
    form = CustomerForm(request.POST or None)
    # Check if form is valid
    if form.is_valid():
        # Save instance
        instance = form.save(commit=False)
        instance.user = request.user
        instance.modified_by = str(request.user)
        instance.save()
        # Message success
        messages.success(request, "Successfully Created")
        # Redirect to detail view
        return HttpResponseRedirect(instance.get_absolute_url())

    # Set context variables
    context = {
        "form":form,
    }
    return render(request, "customer_form.html", context)

def customer_detail(request, id):
    '''
    View for Customer object details including address info and workorders
    '''
    # set global variables
    instance=get_object_or_404(Customer,id=id)
    queryset_list = instance.workorder_set.all()
    paginator = Paginator(queryset_list, 15) # show 15 customers per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer deliver first page
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        queryset = paginator.page(paginator.num_pages)

    # Set context variables
    context ={
            "title":"Customer Info:",
            "instance":instance,
            "lat":instance.lat,
            "lng":instance.lng,
            "workorder":queryset,
            "page_request_var": page_request_var,

    }

    return render(request, "customer_detail.html", context)


def customer_update(request, id=None):
    '''
    View for updating customer object
    '''
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404


    instance=get_object_or_404(Customer,id=id)
    # Load Customer Form
    form = CustomerForm(request.POST or None, instance=instance)
    # Check if form is valid
    if form.is_valid():
        # Save instance
        instance = form.save(commit=False)
        instance.modified_by=str(request.user)
        instance.save()
        # Message success
        messages.success(request, "Successfully Updated")
        # Redirect to detail view
        return HttpResponseRedirect(instance.get_absolute_url())


    context ={
        "title":"Customer Info:",
        "instance":instance,
        "form":form
        }
    return render(request, "customer_form.html", context)


def customer_delete(request, id=None):
    """
    View for Deleting a Customer object
    :param request:
    :param id:
    :return:
    """

    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404


    instance=get_object_or_404(Customer,id=id)
    instance.delete()
    # Message success
    messages.success(request, "Successfully Deleted")
    return redirect("customers:list")


#################### WORKORDER VIEWS ###################


def workorder_create(request, id=None):
    '''
    View for creating a work order Object
    '''
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404


    # Load data from customer
    instance=get_object_or_404(Customer,id=id)

    # Load Work Order Form
    form = WorkOrderForm(request.POST or None, request.FILES or None)
    form.fields["customer_id"].initial= instance.id
    form.fields["customer_id"].disabled=True


    form.fields["latlng"].disabled=True
    form.fields["lat"].disabled=True
    form.fields["lng"].disabled=True

    form.fields["latlng"].widget = forms.HiddenInput()
    form.fields["lat"].widget =  forms.HiddenInput()
    form.fields["lng"].widget =  forms.HiddenInput()
    form.fields["customer_id"].widget =  forms.HiddenInput()

    # Check if form is valid
    if form.is_valid():
        # Save instance
        instance = form.save(commit=False)
        instance.user = request.user
        instance.modified_by = str(request.user)
        instance.save()
        # Message success
        messages.success(request, "Successfully Created")
        # Redirect to detail view
        return HttpResponseRedirect(instance.get_absolute_url())

    # Set context variables
    context={
        "form":form,
        "instance":instance,
    }
    return render(request, "workorder_form.html", context)


def workorder_detail(request, id, jobId):
    '''
    View for Customer object details including address info and workorder
    '''

    # set global variables
    instance=get_object_or_404(Customer,id=id)
    queryset = instance.workorder_set.filter(jobId=jobId)


    # Set context variables
    context ={
            "workorder_title":"Work Order Info:",
            "instance":instance,
            "lat":instance.lat,
            "lng":instance.lng,
            "queryset":queryset,
            }

    return render(request, "workorder_detail.html", context)

def workorder_update(request, id=None, jobId=None):

    '''
    View for updating workorder object
    '''
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404

    instance = get_object_or_404(WorkOrder, customer_id=id, jobId=jobId)
    # Load workorder Form
    form = WorkOrderForm(request.POST or None, request.FILES or None, instance=instance)
    # Check if form is valid
    if form.is_valid():
        # Save instance
        instance = form.save(commit=False)
        instance.modified_by = str(request.user)
        instance.save()
        # Message success
        messages.success(request, "Successfully Updated")
        # Redirect to detail view
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "Work Order Info:",
        "instance": instance,
        "form": form
    }
    return render(request, "workorder_form.html", context)



def workorder_delete(request, id=None, jobId=None):
    """
     View for Deleting a workorder Object
    :param request: httpRequest
    :param id: Customer.id
    :param jobId: wordorder.jobId
    :return:
    """
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404


    instance=get_object_or_404(WorkOrder, customer_id=id, jobId=jobId)
    instance.delete()
    # Message success
    messages.success(request, "Successfully Deleted")
    return HttpResponseRedirect(instance.get_absolute_url())


def confirm_delete(request):
    workorder_delete(request, id=None, jobId=None)