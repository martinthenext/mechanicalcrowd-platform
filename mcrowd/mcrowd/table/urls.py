from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TablesView, TableView, TasksView
from rest_framework.routers import DefaultRouter


urlpatterns = (
    url(r'^$', TablesView.as_view()),
    url(r'(?P<pk>\d+)$', TableView.as_view()),
    url(r'(?P<table>\d+)/tasks$', TasksView.as_view()),
)
