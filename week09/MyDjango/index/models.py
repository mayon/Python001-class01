from django.db import models

# Create your models here.
class Comment(models.Model):
    uname = models.CharField(max_length=50)
    stars = models.IntegerField()
    time = models.CharField(max_length=50, blank=True, null=True)
    votes = models.IntegerField(blank=True, null=True)
    short = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'comment'
