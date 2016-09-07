from __future__ import unicode_literals
from django.conf import settings
from django.db import models
import geocoder
from django.core.urlresolvers import reverse

# Create your models here.
# MVC

class Customer(models.Model):
    NOTAPP ='NA'
    ANGIESLIST='AL'
    CONTRACTOR = 'CO'
    GOOGLE='GO'
    OLDCUST= 'OC'
    OTHER = 'OT'
    RECCO = 'RC'
    REALTOR = 'RE'
    WEBSITE = 'WS'
    YELP = 'YL'

    SOURCE_CHOICES=(
        (NOTAPP,'Not Applicable'),
        (ANGIESLIST, 'Angie\'s List'),
        (CONTRACTOR, 'Contractor'),
        (GOOGLE,'Google'),
        (OLDCUST,'Old Customer'),
        (OTHER,'Other'),
        (RECCO,'Recco'),
        (REALTOR,'Realtor'),
        (WEBSITE,'Website'),
        (YELP,'Yelp'),
    )


    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    modified_by=models.CharField(max_length=50,default=1)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    fullName = models.CharField(max_length=50, blank=True)
    billStreet = models.CharField(max_length=25)
    billCity = models.CharField(max_length=20)
    billState = models.CharField(max_length=2)
    billZip = models.CharField(max_length=5)
    latlng = models.CharField(blank=True, max_length=100)
    lat = models.FloatField(blank=True,max_length=100)
    lng = models.FloatField(blank=True, max_length=100)
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
        return reverse("customers:detail", kwargs={"id": self.id})

    def edit_url(self):
        return reverse("customers:edit", kwargs={"id":self.id})

    class Meta:
        ordering = ["-created", "-modified"]

def upload_location(instance, filename):
    return "%s/%s" % (instance.jobId, filename)

class WorkOrder(models.Model):

    EVAN = 'Evan'
    CHALIE = 'Chalie'
    JOHN = 'John'
    BARRY = 'Barry'
    SERVICE = 'Service'
    JAKE = 'Jake'
    COREY = 'Corey'
    CHRIS = 'Chris'
    SUB = 'Sub'


    LEAD_ASSIGNED_CHOICES = (
        (EVAN, 'Evan'),
        (CHALIE, 'Chalie'),
        (JOHN, 'John'),
        (BARRY, 'Barry'),
        (SERVICE, 'Service'),
    )

    JOB_ASSIGNED_CHOICES = (
        (EVAN, 'Evan'),
        (CHALIE, 'Chalie'),
        (JOHN, 'John'),
        (BARRY, 'Barry'),
        (SERVICE, 'Service'),
        (JAKE, 'Jake'),
        (COREY, 'Corey'),
        (CHRIS, 'Chris'),
        (SUB, 'Sub'),
    )


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
    problem = models.CharField(max_length=200)
    notes = models.CharField(max_length=150, blank=True)
    picture = models.ImageField(null=True,blank=True)
    schedule_date = models.DateField(null=True,blank=True)
    assigned_to = models.CharField(choices=LEAD_ASSIGNED_CHOICES,max_length=20, blank=True, default="")
    contract = models.FileField(upload_to=upload_location, blank=True)
    crew_assigned = models.CharField(choices=JOB_ASSIGNED_CHOICES ,max_length=50, blank=True, default="")
    completed = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    latlng = models.CharField(blank=True, max_length=100, default="")
    lat = models.FloatField(blank=True, max_length=100, default=0)
    lng = models.FloatField(blank=True, max_length=100, default=0)

    class Meta:
        ordering = ["-created", "-modified"]

    # Geocode Full Address and Save
    def save(self, *args, **kwargs):
        full_address = str(self.jobStreet + " " + self.jobCity + " " + self.jobState + " " + self.jobZip)
        g = geocoder.google(full_address)
        lat = str(g.json['lat'])
        lng = str(g.json['lng'])
        self.lat = lat
        self.lng = lng
        self.latlng = lat + "," + lng
        super(WorkOrder, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.jobStreet

    def __str__(self):
        return self.jobStreet

    def __delete__(self, instance):
        return reverse("customers:detail", args=[str(self.customer_id)])

    def get_absolute_url(self):
        return reverse("customers:detail", args=[str(self.customer_id)])




