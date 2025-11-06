from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import BaseModel

# Create your models here.
class Company(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    address = models.CharField(max_length=255)
    website = models.URLField(max_length=54, blank=True)
    vat_number = models.CharField(max_length=9)
    createdBy = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="companies_created",
        null=True, blank=True
    )