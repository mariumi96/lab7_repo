# coding=utf-8
from django.shortcuts import render
from .models import Question
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import Http404, JsonResponse
# django imports
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
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

def singup(request):
    errors = []
    formdata = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            errors.append("Введите имя пользователя")
        elif len(username) < 5:
            errors.append("Имя пользователя должно содержать не менее 5 символов")

        email = request.POST.get('email')
        if not email:
            errors.append("Введите адрес эл. почты")

        firstname = request.POST.get('firstname')
        if not firstname:
            errors.append("Введите своё имя")
        else:
            formdata['firstname'] = firstname

        lastname = request.POST.get('lastname')
        if not lastname:
            errors.append("Введите своё фамилию")
        else:
            formdata['lastname'] = lastname

        password = request.POST.get('password')
        if not password:
            errors.append("Введите пароль")
        elif len(password) < 8:
            errors.append("Пароль должен содержать не менее 8 символов")
        else:
            confirmpass = request.POST.get('confirmpass')
            if not confirmpass:
                errors.append("Подтвердите пароль")
            elif password != confirmpass:
                errors.append("Пароли не совпадают")
                formdata['confirmpass'] = confirmpass
            formdata['password'] = password

        sameusers = []
        try:
            sameusers.append(User.objects.get(username=username))
        except User.DoesNotExist:
            formdata['username'] = username
        try:
            sameusers.append(User.objects.get(email=email))
        except User.DoesNotExist:
            formdata['email'] = email

        if sameusers:
            errors.append("Пользователь с таким именем или адресом эл. почты уже существует")

        if errors:
            return render(request, 'singup.html', {'errors': errors, 'formdata': formdata})

        User.objects.create_user(username=username, email=email, password=password)
        return HttpResponseRedirect("/login/")

    return render(request, 'singup.html', {'errors': [], 'formdata': formdata})


#def login(request):
#    return render(request, 'login.html')


def add_user(request, context):
    usr = User.objects.filter(id=request.user.id).last()
    context['userinfo'] = usr
    return context


def singin2(request):
    # check if continue exists
    continue_path = request.GET.get("continue", '/questions')
    # if user is authenticated, then redirect him to info page
    if request.user.is_authenticated:
        context = {}
        context = add_user(request, context)
        # add a continue path for the user to go back
        context["continue"] = continue_path
        return render(request, 'questions.html', context) #singed_in
    # if a user just wants to login
    continue_path = request.GET.get("continue", '/questions')
    if request.method == 'GET':
        form = LoginForm()
    else: # else, if he sends some data in POST
        form = LoginForm(request.POST) # initialize the form with POST data
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request=request, username=username, password=password) # try auth
            if user is not None: # if auth is success
                login(request, user) # start session
                return redirect('/questions') #redirect to continue or to /
            else: # else, auth gone wrong
                form.add_error(None, "Username or password is incorrect")

    return render(request, 'login.html', {'form': form})


def singin(request):
    # check if continue exists
    continue_path = request.GET.get("continue", '/')
    # if user is authenticated, then redirect him to info page
    if request.user.is_authenticated:
        context = {}
        context = add_user(request, context)
        # add a continue path for the user to go back
        context["continue"] = continue_path

    # if a user just wants to login
    if request.method == 'GET':
        form = LoginForm()
    else: # else, if he sends some data in POST
        form = LoginForm(request.POST) # initialize the form with POST data
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request=request, username=username, password=password) # try auth
            if user is not None: # if auth is success
                login(request, user) # start session
                return redirect(continue_path) #redirect to continue or to /
            else: # else, auth gone wrong
                form.add_error(None, "Username or password is incorrect")

    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.user.is_authenticated:
        context = {}
        context = add_user(request, context)
        return render(request, 'questions.html', context)#singed_in
    if request.method == 'GET':
        register_form = RegisterForm()
    else:
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            new_profile = register_form.save()
            login(request, new_profile)
            return redirect('index')
    return render(request, 'singup.html', {'form': register_form})


@login_required()
def log_out(request):
    continue_path = request.GET.get("continue", '/questions')
    logout(request)
    return redirect('/questions')