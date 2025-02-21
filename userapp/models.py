from django.contrib.auth.models import User
from django.db import models

from testbookapp.models import bookprofile


class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    items=models.ManyToManyField(bookprofile)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    book=models.ForeignKey(bookprofile,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)


