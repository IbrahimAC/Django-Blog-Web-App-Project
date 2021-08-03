from django.db import models
from django.db.models.fields import PositiveIntegerField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

#class is a table, the variables are the attributes
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk}) 

class addressbook(models.Model):
    name = models.CharField(max_length=100)
    street_name = models.TextField()
    door_number = models.PositiveIntegerField()
    postcode = models.CharField(max_length=10)


     