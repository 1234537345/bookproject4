#from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField


class bookprofile(models.Model):
    bookname = models.CharField(max_length=200)
    bookprice = models.IntegerField()
    author = models.CharField(max_length=200, blank=True, null=True)
    bookimage = models.ImageField(upload_to='book_media', null=True, blank=True)
    quantity=models.IntegerField(blank=True, null=True)

def __str__(self):
    return '{}'.format(self.bookname)













