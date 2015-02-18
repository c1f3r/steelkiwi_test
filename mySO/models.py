from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

from mySO.signals import notify_author_about_new_comment


class Question(models.Model):
    subject = models.CharField(max_length=200)
    question = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return u"{0} by {1}".format(self.subject, self.author)

    def get_absolute_url(self):
        return reverse('question_detail', args=[str(self.id)])


class Comment(models.Model):
    question = models.ForeignKey(Question)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return u'{0} on {1} at {2}'.format(self.author.username,
                                           self.question.subject,
                                           self.timestamp.strftime(
                                               "%d %b %Y %H:%M:%S"))

post_save.connect(notify_author_about_new_comment, sender=Comment)
