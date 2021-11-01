from django.db import models

# Create your models here.

class City(models.Model):
    name_en = models.CharField(max_length=30)
    name_ar = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.name_en  + ' | ' + self.name_ar
    
    class Meta:
        verbose_name_plural = 'Cities'