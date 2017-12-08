from django.db import models
from django.utils import timezone
# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=60)
    text = models.TextField()
    snippet = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    author = models.CharField(max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    question = models.ForeignKey(Question)
    rating = models.IntegerField(default=0)


