from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from mySO.views import QuestionListView, NewQuestionView, QuestionDetailView, \
    AddCommentView


urlpatterns = patterns('',
                       url(r'^$', QuestionListView.as_view(), name='index'),
                       url(r'^new_question/$', NewQuestionView.as_view(),
                           name='new_question'),
                       url(r'^question/(?P<pk>\d+)/$',
                           QuestionDetailView.as_view(),
                           name='question_detail'),
                       url(r'^question/(?P<question_id>\d+)/add_comment/$',
                           login_required(AddCommentView.as_view()),
                           name='add_comment'),
                       )


# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
