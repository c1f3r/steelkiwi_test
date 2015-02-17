from django.core.mail import send_mail


def notify_author_about_new_comment(sender, instance, **kwargs):
    send_mail('You have new comment on mySO site',
              '{0} posted comment on your "{1}" question'.format(
                  instance.author.username, instance.question.subject),
              'ciferstov@gmail.com', instance.question.author.email)