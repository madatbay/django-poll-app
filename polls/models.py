from django.db import models
from django.utils import timezone
from django.conf import settings 
import datetime

User = settings.AUTH_USER_MODEL 

# Create your models here.

class Question(models.Model):
    user = models.ForeignKey(User, default=1, null= True, on_delete = models.SET_NULL)
    question_text = models.CharField(max_length=70)
    describtion = models.TextField(null=True, max_length=200)
    pub_date = models.DateTimeField(auto_now=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Voter(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    poll = models.ForeignKey(Question, on_delete = models.CASCADE)