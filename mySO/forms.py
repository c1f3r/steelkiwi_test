from django.forms import ModelForm
from mySO.models import Comment


class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [u'comment']