from django.db import models
import os


class People(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    work = models.CharField(max_length=13)
    gender = models.IntegerField()
    faceImg = models.FileField(upload_to='all_face')

    def __str__(self):
        return self.firstName




class Visits(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE, related_name='people')
    visiting_time = models.DateTimeField(auto_now_add=True)
    countOFvisits = models.IntegerField(null = False, blank = False, default=0)





