from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^api/v1/auth/token/',
        'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api/v1/xlsx/', include('mcrowd.xlsx.urls')),
    url(r'^api/v1/task/', include('mcrowd.task.urls')),
    url(r'^api/v1/mturk/', include('mcrowd.mturk.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
