from django.db import models
from main.models import CustomUser




class Courier(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=200)
    expirience = models.PositiveIntegerField()
    rating = models.FloatField()


    def __str__(self) -> str:
        return f'{self.name}-{self.rating}'