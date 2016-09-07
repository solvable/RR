import datetime
from haystack import indexes
from .models import Customer

class CustomerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document = True, use_template=True)
    billStreet = indexes.CharField(model_attr='billStreet')
    billCity = indexes.CharField(model_attr = 'billCity')
    billState = indexes.CharField(model_attr = 'billState')
    billZip = indexes.CharField(model_attr = 'billZip')
    phone1 = indexes.CharField(model_attr='phone1')
    phone2 = indexes.CharField(model_attr='phone2')
    email = indexes.CharField(model_attr='email')


    def get_model(self):
        return Customer

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated"""
        return self.get_model().objects

