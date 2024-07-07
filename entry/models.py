from django.db import models

# Create your models here.
class Entries (models.Model):
    entry_id = models.AutoField (primary_key = True) 
    user_id = models.IntegerField()
    date_created = models.DateTimeField (auto_now_add = True)
    date_updated = models.DateTimeField (auto_now = True)
    title = models.CharField (max_length = 25, null = False, blank = False)
    content = models.TextField(null = False, blank = False)

    def __str__(self):
        if self.date_created == self.date_updated:
            f"{self.title} - {self.date_created}"
        else:
            return f"{self.title} - {self.date_created} [{self.date_updated}]"