from django.db import models

# Create your models here.

from django.db import models
class Patient(models.Model):
   name = models.CharField(max_length=30)
   mail = models.CharField(max_length=30)
   def __str__(self):
      return self.name

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class WoundInfo(models.Model):
   depth = models.CharField(max_length=30)
   category = models.CharField(max_length=30)
   type = models.CharField(max_length=30)
   area = models.CharField(max_length=30)
   diameter = models.CharField(max_length=30)
   additional = models.CharField(max_length=100)
   image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)

class Wound(models.Model):
   patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
   wound_info = models.ForeignKey(WoundInfo, on_delete=models.CASCADE)

   def __str__(self):
      return self.additional
