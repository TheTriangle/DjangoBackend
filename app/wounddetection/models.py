from django.db import models

# Create your models here.

from django.db import models

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Specialization(models.Model):
   name = models.CharField(max_length=30)

class Doctor(models.Model):
   email = models.CharField(max_length=30)
   name = models.CharField(max_length=30)
   specialization = models.CharField(max_length=30) #TODO replace with Specialization mdel


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
   doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
   reports = models.ManyToManyField(WoundReport)


class Patient(models.Model):
   name = models.CharField(max_length=30)
   mail = models.CharField(max_length=30)
   cases = models.ManyToManyField(Case)
   def __str__(self):
      return self.name