from django.conf.urls import patterns, url
from .views import QuestionView


urlpatterns = (
    url(r'^question/$', QuestionView.as_view(), name='question'),
)

