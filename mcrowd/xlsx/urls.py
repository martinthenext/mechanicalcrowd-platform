from django.conf.urls import patterns, url
from .views import TablesView, TableView

urlpatterns = (
    url(r'^/$', TablesView.as_view()),
    url(r'(?P<pk>\d+)/$', TableView.as_view()),
)
