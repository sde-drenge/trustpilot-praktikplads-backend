from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from user.models import BaseModel

# Create your models here.

class Review(BaseModel):
    title = models.CharField(max_length=54)
    student = models.ForeignKey("user.User", on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    isApproved = models.BooleanField(default=True)
