from django.db import models
from django.urls import reverse

class Computer(models.Model):
    '''
    description: This class creates a computer and its properties
    properties:
      make: The make will contain the name of the brand of the computer.
      manufacturer: The manufacturer will contain the name of the company who manufactured the computer.
      purchase_date: This property contains the purchase date in string form.
      decomission_date: This property contains the dicomission date in string form.
    '''

    make = models.CharField(max_length=20)
    manufacturer = models.CharField(max_length=20, default=None)
    purchase_date = models.DateField()
    decommission_date = models.DateField(null=True, blank=True, default=None)

    class Meta:
        verbose_name = ("Computer")
        verbose_name_plural = ("Computers")

    def get_absolute_url(self):
        return reverse("Computer_detail", kwargs={"pk": self.pk})
