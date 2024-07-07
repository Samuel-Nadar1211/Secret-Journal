from django.db import models

# Create your models here.
class User (models.Model):
    user_id = models.AutoField (primary_key = True)
    name = models.CharField (max_length = 25, null = False, blank = False)
    email = models.EmailField (max_length = 50, unique = True, null= False, blank = False)
    password = models.CharField (max_length = 25, null = False, blank = False)