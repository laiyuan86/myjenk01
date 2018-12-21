from django.db import models

# Create your models here.


class Jobsnamedes(models.Model):
    jobname = models.CharField(max_length=100)
    jobdesc = models.CharField(max_length=200)


class Buildhistory(models.Model):
    buildtime = models.DateTimeField()
    buildnum = models.IntegerField()
    status = models.CharField(max_length=100)
    jobname = models.ForeignKey(Jobsnamedes, on_delete=models.CASCADE)
