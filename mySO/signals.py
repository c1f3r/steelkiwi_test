from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site


def notify_author_about_new_comment(sender, instance, **kwargs):
    subject = u'You have new comment on mySO site'
    from_email = u'ciferstov@gmail.com'
    to = instance.question.author.email
    text_content = u'{0} posted comment on your "{1}" question'.format(
        instance.author.username, instance.question.subject)
    html_content = u'''<p>{0} posted new comment on your
                    <a href="http://{1}{2}">{3}</a> question</p>
                    <p>{4}</p>'''.format(instance.author.username,
                                         Site.objects.get_current().domain,
                                         instance.question.get_absolute_url(),
                                         instance.question.subject,
                                         instance.comment)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
