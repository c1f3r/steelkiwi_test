from django.contrib.auth.models import User

from mySO.models import Question, Comment


def create_question(subject, question, author_username):
    return Question.objects.create(subject=subject, question=question,
                                   author=User.objects.get(
                                       username=author_username))


def create_comment(comment, question, author_username):
    return Comment.objects.create(comment=comment, question=question,
                                  author=User.objects.get(
                                      username=author_username))
