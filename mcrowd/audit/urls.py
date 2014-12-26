from django.conf.urls import patterns, url
from .views import LogView


urlpatterns = (
    url(r'^$', LogView.as_view(), name='log'),
)
