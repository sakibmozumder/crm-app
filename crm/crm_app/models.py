from django.db import models

# Create your models here.


class Client(models.Model):
    dateCreated = models.DateTimeField(auto_now_add=True)
    company = models.CharField(max_length=50)
    clientCode = models.IntegerField(primary_key=True, unique=True)
    address = models.CharField(max_length=100)
    assigned_personnel = models.CharField(max_length=50)
    personnelID = models.IntegerField()

    def __str__(self) -> str:
        return (f"{self.company}")


class Personnel(models.Model):
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    username = models.CharField(max_length=50)
    personnelID = models.IntegerField()

    def __str__(self) -> str:
        return (f"{self.firstname} {self.lastname}")
