from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class ShellModel(models.Model):
    userID = models.CharField(max_length=255, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'shell'
        ordering = ['-createdAt']
        def __str__(self) -> str:
            return self.userID