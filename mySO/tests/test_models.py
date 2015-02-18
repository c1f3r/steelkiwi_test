from django.test import TestCase
from django.core import mail

from mySO.tests.common import create_question, create_comment


class TestQuestion(TestCase):
    fixtures = [u'initial_data.json']

    def test_question_string_representation(self):
        question = create_question(subject=u'First Question',
                                   question=u'This is the First Question',
                                   author_username=u'admin')
        self.assertEqual(u'First Question by admin', unicode(question))

    def test_absolute_url_for_question(self):
        first_question = create_question(
            subject=u'First Question',
            question=u'This is the First Question',
            author_username=u'admin')
        second_question = create_question(
            subject=u'Second Question',
            question=u'This is the Second Question',
            author_username=u'tester')
        self.assertEqual(u'/question/1/', first_question.get_absolute_url())
        self.assertEqual(u'/question/2/', second_question.get_absolute_url())


class TestComment(TestCase):
    fixtures = [u'initial_data.json']

    def test_comment_string_representation(self):
        question = create_question(
            subject=u'First Question', question=u'This is the First Question',
            author_username=u'admin')
        comment = create_comment(
            comment=u'First Comment', question=question,
            author_username=u'tester')
        self.assertIn(u'tester on First Question at ', unicode(comment))

    def test_email_is_sent_when_comment_added(self):
        question = create_question(
            subject=u'First Question', question=u'This is the First Question',
            author_username=u'admin')
        create_comment(
            comment=u'First Comment', question=question,
            author_username=u'tester')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [u'admin@myso.com'])
        question = create_question(
            subject=u'First Question', question=u'This is the First Question',
            author_username=u'tester')
        create_comment(
            comment=u'First Comment', question=question,
            author_username=u'admin')
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].to, [u'tester@myso.com'])
