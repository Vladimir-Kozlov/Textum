from django.conf.urls import patterns, include, url

from textum.textedit import views


urlpatterns = patterns('',
    url(r'^$', views.TextEdit.as_view(), name='main'),
    url(r'^fullView$', views.fullView, name='fullView'),
    url(r'^upload$', views.RTFCreateView.as_view(), name='upload'),
)