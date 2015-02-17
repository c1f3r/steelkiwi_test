from django.contrib.auth.models import User
from django.db import models


# from signals import notify_author_about_new_comment
# Create your models here.


class Question(models.Model):
    subject = models.CharField(max_length=200)
    question = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.subject


class Comment(models.Model):
    question = models.ForeignKey(Question)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)

# comment_was_posted.connect(notify_author_about_new_comment)
