
# Create your views here.
from django import http
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import ListView, CreateView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from mySO.models import Question, Comment


class QuestionListView(ListView):
    model = Question
    context_object_name = u"questions"
    paginate_by = 5


class NewQuestionView(CreateView):
    model = Question
    fields = [u"subject", u"question"]

    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.save()
        return http.HttpResponseRedirect(reverse(u'index'))


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [u'comment']


class QuestionDetailView(DetailView):
    model = Question
    context_object_name = u'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.all()
        context['comment_form'] = CommentForm()
        return context


class AddCommentView(FormView):
    form_class = CommentForm

    def get_success_url(self):
        # Redirect to previous url, which means the detail page
        # Since there is a bug about using success_url with reverse
        # See: http://djangosnippets.org/snippets/2445/
        # get_success_url should be used with FormView
        return self.request.META.get('HTTP_REFERER', None)

    def form_valid(self, form):
        # if form is valid, then save data to the database
        # access question_id parameter through self.kwargs
        comment = Comment(
            question=Question.objects.get(pk=int(self.kwargs['question_id'])),
            author=self.request.user)
        comment_form = CommentForm(self.request.POST, instance=comment)
        comment_form.save()
        return super(AddCommentView, self).form_valid(comment_form)

    def form_invalid(self, form):
        # if invalid, then stay in the detail page
        return self.render_to_response(
            self.get_context_data(comment_form=form,
                                  question=Question.objects.get(
                                      pk=int(self.kwargs['question_id']))))