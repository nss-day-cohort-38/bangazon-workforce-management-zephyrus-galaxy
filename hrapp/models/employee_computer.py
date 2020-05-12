from django.db import models
from ..models import Employee, Computer
from django.urls import reverse

class EmployeeComputer(models.Model):

    # Creates the join table for the many to many relationship between computers and employees

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    assign_date = models.DateField(default=None)
    unassign_date = models.DateField(default=None)
    
    class Meta:
        verbose_name = ("employee_computer")
        verbose_name_plural = ("employee_computers")
    def __str__(self):
        return f"{self.employee} {self.computer}"

    def get_absolute_url(self):
        return reverse("employee_computer_detail", kwargs={"pk": self.pk})