
# Create your views here.
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms import ModelForm
from django.views.generic import ListView, CreateView, DetailView, FormView

from mySO.models import Question, Comment


class QuestionListView(ListView):
    model = Question
    context_object_name = u"questions"
    paginate_by = 5


class NewQuestionView(CreateView):
    model = Question
    fields = [u"subject", u"question"]
    success_url = reverse_lazy(u'index')

    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.save()
        return super(NewQuestionView, self).form_valid(form)


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
        return reverse(u'question_detail',
                       args=(int(self.kwargs['question_id']), ))

    def form_valid(self, form):
        # if form is valid, then save data to the database
        # access question_id parameter through self.kwargs
        comment = Comment(
            question=Question.objects.get(pk=int(self.kwargs['question_id'])),
            author=self.request.user)
        comment_form = CommentForm(self.request.POST, instance=comment)
        comment_form.save()
        return super(AddCommentView, self).form_valid(comment_form)
