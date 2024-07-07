from django.db import models

# Create your models here.
class Events (models.Model):
    event_id = models.AutoField (primary_key = True) 
    user_id = models.IntegerField()
    title = models.CharField (max_length = 25, null = False, blank = False)
    date = models.DateField(null = False, blank = False)
    is_anniversary = models.BooleanField(null = False, blank = False)
    remark = models.TextField()

    def __str__(self):
        return self.title