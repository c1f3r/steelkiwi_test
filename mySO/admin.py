from django.contrib import admin

# Register your models here.
from mySO.models import Question, Comment



class CommentAdmin(admin.TabularInline):
    model = Comment


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [CommentAdmin]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass