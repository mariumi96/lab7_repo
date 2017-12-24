from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^questions/$', views.index, name='index'),
    url(r'^questions/(?P<id>(\d+))$', views.question, name='question'),
    url(r'^singup/$', views.singup, name='singup'),
    url(r'^login/$', views.singin, name='login'),
    url(r'^logout/$', views.log_out, name="logout")
]