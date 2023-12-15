from django.db import models
from main.models import CustomUser



class Courier(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    status_choices = [
        ('Свободен', 'FREE'),
        ('Занят', 'BUSY'), 
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Свободен')
    expirience = models.PositiveIntegerField()
    rating = models.FloatField(default=0)


    def __str__(self) -> str:
        return f'{self.user.first_name}-{self.status}'