
from shop.models import *


class Person(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fname = models.CharField(null=True, blank=True, max_length=30)
    lname = models.CharField(null=True, blank=True, max_length=30)
    region = models.CharField(null=True, blank=True, max_length=50)
    city = models.CharField(null=True, blank=True, max_length=50)
    street = models.CharField(null=True, blank=True, max_length=50)
    house_number = models.CharField(null=True, blank=True, max_length=10)
    appartments_number = models.CharField(null=True, blank=True, max_length=10)
    zipcode = models.CharField(null=True, blank=True, max_length=10)


class Favorites(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    fav_item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.fav_item.name
