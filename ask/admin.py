from django.contrib import admin
from ask import models

class QuestionAdmin(admin.ModelAdmin):
    list_display=('title',)

class AnswerAdmin(admin.ModelAdmin):
    list_display=('author',)

admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
# Register your models here.
