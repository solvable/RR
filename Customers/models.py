from __future__ import unicode_literals
from django.conf import settings
from django.db import models
import geocoder
from django.core.urlresolvers import reverse
from .choices import *
from schedule.models import Event, EventRelation, Calendar
import datetime
from datetime import timedelta
# Create your models here.
# MVC



class Customer(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    modified_by=models.CharField(max_length=50,default=1)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    fullName = models.CharField(max_length=50, blank=True)
    billStreet = models.CharField(max_length=25)
    billCity = models.CharField(max_length=20)
    billState = models.CharField(max_length=2)
    billZip = models.CharField(max_length=5)
    latlng = models.CharField(blank=True, max_length=100, default = '')
    lat = models.FloatField(blank=True,max_length=100, default = '')
    lng = models.FloatField(blank=True, max_length=100, default='')
    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    source = models.CharField(choices=SOURCE_CHOICES, max_length=20, default=NOTAPP)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Geocode Full Address
    def save(self, *args, **kwargs):
        full_address = str(self.billStreet + " " + self.billCity + " " + self.billState + " " + self.billZip)
        g = geocoder.google(full_address)
        lat = str(g.json['lat'])
        lng = str(g.json['lng'])
        self.fullName = str(self.firstName+" "+self.lastName)
        self.lat = lat
        self.lng = lng
        self.latlng = lat + "," + lng

        super(Customer, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("customers:customer_detail", kwargs={"id": self.id})

    def edit_url(self):
        return reverse("customers:customer_edit", kwargs={"id":self.id})

    class Meta:
        ordering = ["-created", "-modified"]

def upload_location(instance, filename):
    return "%s/%s" % (instance.jobId, filename)

class Jobsite(models.Model):

    customer_id = models.ForeignKey(
        'Customer',
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    modified_by = models.CharField(max_length=50, default=1)
    jobId= models.AutoField(primary_key=True)
    jobStreet = models.CharField(max_length=25)
    jobCity = models.CharField(max_length=20)
    jobState = models.CharField(max_length=2)
    jobZip = models.CharField(max_length=5)
    stories = models.IntegerField()
    access = models.CharField(max_length=20)
    notes = models.CharField(max_length=150, blank=True)
    picture = models.ImageField(null=True,blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    latlng = models.CharField(blank=True, max_length=100, default="")
    lat = models.FloatField(blank=True, max_length=100, default=0)
    lng = models.FloatField(blank=True, max_length=100, default=0)
    class Meta:
        ordering = ["-created", "-modified"]




    # Geocode Full Address and Save
    def save(self, *args, **kwargs):
        # Geolocate
        full_address = str(self.jobStreet + " " + self.jobCity + " " + self.jobState + " " + self.jobZip)
        g = geocoder.google(full_address)
        lat = str(g.json['lat'])
        lng = str(g.json['lng'])
        self.lat = lat
        self.lng = lng
        self.latlng = lat + "," + lng
        super(Jobsite, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.jobId

    def __str__(self):
        return self.jobId

    def __delete__(self, instance):
        return reverse("customers:customer_detail", args=[str(self.customer_id)])

    def get_absolute_url(self, *args,**kwargs):
        return reverse("customers:jobsite_detail", args=[str(self.customer_id), str(self.jobId)])


class Appointment(models.Model):
    appId = models.AutoField(primary_key=True)
    jobsite_id = models.ForeignKey(
        'Jobsite',
    )
    title = models.CharField(null=True, blank=True, choices=TITLES,max_length=10)
    problem = models.CharField(max_length=200)

    schedule_date = models.DateField(null=True, blank=True)
    time_slot = models.CharField(blank=True, choices=TIME_SLOTS, default='', max_length=20, null=True)
    start = models.CharField(null=True, max_length=30, blank=True)
    end = models.CharField(null=True, max_length=30, blank=True)
    appt = models.CharField(null=True, max_length=70, blank=True)

    assigned_to = models.CharField(choices=LEAD_ASSIGNED_CHOICES,max_length=20, blank=True, default="")
    contract = models.FileField(upload_to=upload_location, blank=True)

    completed = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    modified_by = models.CharField(max_length=50, default=1, null=True)
    notes = models.TextField(max_length=200, default='', null=True)
    def save(self, *args, **kwargs):

        if self.time_slot == t0810:
            start = "8:00"
            end = "10:00"
        elif self.time_slot == t0911:
            start = "9:00"
            end = "11:00"
        elif self.time_slot == t1012:
            start = "10:00"
            end = "12:00"
        elif self.time_slot == t1113:
            start = "11:00"
            end = "13:00"
        elif self.time_slot == t1214:
            start = "12:00"
            end = "14:00"
        elif self.time_slot == t1315:
            start = "13:00"
            end = "15:00"
        else:
            start = "14:00"
            end = "16:00"
        self.start = start
        self.end = end

        if self.appt:
            self.appt=''

        self.appt = str("{title:'" + str(self.title) +"', start:'"+ str(self.schedule_date) +"T"+(self.start) +"', end:'"+ str(self.end) + "'}")
        super(Appointment, self).save(*args, **kwargs)

    def __unicode(self):
        return str(self.schedule_date)


    def __str__(self):
        return str(self.schedule_date)

    def __delete__(self, instance):
        return reverse("customers:index")

    def get_absolute_url(self, kwargs):

        return reverse("customers:appointment_detail", kwargs={"id":u'id, "jobId":u'self.jobsite_id,"appId":strself.appId})