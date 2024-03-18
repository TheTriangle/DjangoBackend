from django.db import models

# Create your models here.

from django.db import models

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Patient(models.Model):
   name = models.CharField(max_length=30)
   mail = models.CharField(max_length=30)
   def __str__(self):
      return self.name

class Specialization(models.Model):
   name = models.CharField(max_length=30)

class Doctor(models.Model):
   email = models.CharField(max_length=30)
   name = models.CharField(max_length=30)
   specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)


class WoundReport(models.Model):
   upload_date = models.DateTimeField(null=True)
   depth = models.CharField(max_length=30)
   category = models.CharField(max_length=30)
   type = models.CharField(max_length=30)
   area = models.CharField(max_length=30)
   diameter = models.CharField(max_length=30)
   additional = models.CharField(max_length=100)
   image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)

class Case(models.Model):
   patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
   doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
   reports = models.ManyToManyField(WoundReport)


WoundReport.case = models.ForeignKey(Case, on_delete=models.CASCADE)
Patient.cases = models.ManyToManyField(Case)


