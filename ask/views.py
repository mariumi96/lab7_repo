from django.shortcuts import render
from .models import Question

# Create your views here..


def index(request):
    questions = Question.objects.all()
    content = {
        'questions': questions
    }
    for q in questions:
        print(q)
    return render(request, 'index.html', content)


def question(request, id):
    q = Question.objects.get(id=int(id))
    content = {
        'question' : q
    }
    return render(request, 'questions.html', content)
