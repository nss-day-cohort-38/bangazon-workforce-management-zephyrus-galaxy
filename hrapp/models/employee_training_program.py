from django.db import models
from .employee import Employee
from .training_program import TrainingProgram
from django.urls import reverse

class EmployeeTrainingProgram(models.Model):

    # Creates the join table for the many to many relationship between training program and employees

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    training_program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE)
 
    class Meta:
        verbose_name = ("employee_training_program")
        verbose_name_plural = ("employee_training_programs")

    def __str__(self):
        return f"{self.employee} {self.computer}"

    def get_absolute_url(self):
        return reverse("employee_training_program_detail", kwargs={"pk": self.pk})