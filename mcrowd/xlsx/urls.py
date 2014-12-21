from django.conf.urls import patterns, url
from .views import WorkbookUploaderView, WorkbookView
from .views import WorksheetsView, WorksheetView
from .views import TablesView, TableView
from .views import SampleView

urlpatterns = (
    url(r'^$', WorkbookUploaderView.as_view(),
        name='workbooks'),
    url(r'^(?P<pk>\d+)/$', WorkbookView.as_view(),
        name='workbook'),
    url(r'^(?P<workbook>\d+)/worksheets/$', WorksheetsView.as_view(),
        name='worksheets'),
    url(r'^(?P<workbook>\d+)/worksheets/(?P<number>\d+)/$',
        WorksheetView.as_view(),
        name='worksheet'),
    url(r'^(?P<workbook>\d+)/worksheets/(?P<number>\d+)/tables/$',
        TablesView.as_view(),
        name='tables'),
    url(r'^(?P<workbook>\d+)/worksheets/(?P<number>\d+)/tables/(?P<pk>\d+)/$',
        TableView.as_view(),
        name='table'),
    url(r'^(?P<workbook>\d+)/worksheets/(?P<number>\d+)/tables/(?P<pk>\d+)/sample/$',
        SampleView.as_view(),
        name='sample'),
)
