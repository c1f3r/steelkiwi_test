from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from mySO.models import Question, Comment
from mySO.tests.common import create_question


class TestIndex(TestCase):
    fixtures = ['initial_data.json']

    def test_index_page_renders_question_list_template(self):
        response = self.client.get(reverse(u"index"))
        self.assertTemplateUsed(response, u'mySO/question_list.html')

    def test_index_page_contains_correct_links_when_not_logged_in(self):
        response = self.client.get(reverse(u'index'))
        self.assertContains(response, reverse(u'auth_login'))
        self.assertContains(response, reverse(u'registration_register'))
        self.assertNotContains(response, reverse(u'new_question'))
        self.assertNotContains(response, reverse(u'auth_logout'))

    def test_index_page_contains_correct_links_when_logged_in(self):
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.get(reverse(u'index'))
        self.assertNotContains(response, reverse(u'auth_login'))
        self.assertNotContains(response, reverse(u'registration_register'))
        self.assertContains(response, reverse(u'new_question'))
        self.assertContains(response, reverse(u'auth_logout'))
        self.assertContains(response, u'Hello, admin')

    def test_index_page_is_not_paginated_until_has_one_questions(self):
        create_question(subject=u'First Question',
                        question=u"This is the First Question",
                        author_username=u'admin')
        response = self.client.get(reverse(u'index'))
        self.assertNotContains(response, u'<a href="?page=2">2</a>')

    def test_index_page_is_paginated_when_has_six_or_eleven_questions(self):
        for i in xrange(6):
            create_question(subject=u'Question',
                            question=u"This is the Question",
                            author_username=u'admin')
        response = self.client.get(reverse(u'index'))
        self.assertContains(response, u'<a href="?page=2">2</a>')
        for i in xrange(5):
            create_question(subject=u'Question',
                            question=u"This is the Question",
                            author_username=u'admin')
        response = self.client.get(reverse(u'index'))
        self.assertContains(response, u'<a href="?page=2">2</a>')
        self.assertContains(response, u'<a href="?page=3">3</a>')


class TestNewQuestionPage(TestCase):
    fixtures = [u'initial_data.json']

    def test_new_question_page_redirects_to_login_page_if_not_logged_in(self):
        response = self.client.get(reverse(u'new_question'))
        next_url = '?next=' + reverse(u'new_question')
        expected_redirect_url = reverse(u'auth_login') + next_url
        self.assertRedirects(response, expected_redirect_url)

    def test_new_question_page_uses_correct_template(self):
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.get(reverse(u'new_question'))
        self.assertTemplateUsed(response, u'mySO/question_form.html')

    def test_new_question_has_been_added_correct(self):
        self.client.login(username=u'admin', password=u'admin')
        self.assertEqual(Question.objects.count(), 0)
        response = self.client.post(reverse(u'new_question'),
                                    {u'subject': u'Question',
                                     u'question': u'This is the Question'})
        self.assertRedirects(response, reverse(u'index'))
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.first().subject, u'Question')
        self.assertEqual(Question.objects.first().author.username, u'admin')


class TestQuestionDetailView(TestCase):
    fixtures = ['initial_data.json']

    def test_question_detail_view_uses_correct_template(self):
        create_question(subject=u'Question',
                        question=u"This is the Question",
                        author_username=u'admin')
        response = self.client.get(reverse(u'question_detail', args=(1, )))
        self.assertTemplateUsed(response, u'mySO/question_detail.html')
        self.assertContains(response, u'<h1>Question</h1>')

    def test_question_detail_page_doesnt_contain_form_when_not_logged_in(self):
        create_question(subject=u'Question',
                        question=u"This is the Question",
                        author_username=u'admin')
        response = self.client.get(reverse(u'question_detail', args=(1, )))
        self.assertContains(response, u'If you want to leave your comment ')
        self.assertNotContains(response, u'id="id_comment"')

    def test_question_detail_page_contains_form_when_logged_in(self):
        create_question(subject=u'Question',
                        question=u"This is the Question",
                        author_username=u'admin')
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.get(reverse(u'question_detail', args=(1, )))
        self.assertNotContains(response, u'If you want to leave your comment ')
        self.assertContains(response, u'id="id_comment"')


class TestAddCommentView(TestCase):
    fixtures = [u'initial_data.json']

    def test_login_redirect_when_trying_add_comment_without_logging_in(self):
        create_question(subject=u'Question',
                        question=u"This is the Question",
                        author_username=u'admin')
        response = self.client.post(
            reverse(u'add_comment', args=(1, )),
            {u'comment': u'Comment'})
        next_url = '?next=' + reverse(u'add_comment', args=(1, ))
        expected_redirect_url = reverse(u'auth_login') + next_url
        self.assertRedirects(response, expected_redirect_url)

    def test_adds_comment_when_logged_in_and_sends_email(self):
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
        create_question(subject=u'Question',
                        question=u"This is the Question",
                        author_username=u'admin')
        self.client.login(username=u'tester', password=u'tester')
        response = self.client.post(
            reverse(u'add_comment', args=(1, )),
            {u'comment': u'This is the Comment'})
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [u'admin@myso.com'])
        expected_redirect_url = reverse(u'question_detail', args=(1, ))
        self.assertRedirects(response, expected_redirect_url)
        response = self.client.get(expected_redirect_url)
        self.assertContains(response, u'<p>tester left at ')
        self.assertContains(response, u'This is the Comment')
