from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^api/v1/auth/token/',
        'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api/v1/auth/refresh/',
        'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^api/v1/tables/', include('mcrowd.table.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
