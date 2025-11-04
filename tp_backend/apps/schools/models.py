from django.db import models
from django.contrib.auth import get_user_model
from user.models import BaseModel

User = get_user_model()

# Create your models here.
class School(BaseModel):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    isActive = models.BooleanField(default=True)
    

    @property
    def students(self):
        return self.users.filter(role=User.Role.STUDENT)

    @property
    def teachers(self):
        return self.users.filter(role=User.Role.TEACHER)


    def __str__(self):
        return self.name
    
    def getSchools(self):
        return School.objects.filter(isActive=True, deletedAt__isnull=True)