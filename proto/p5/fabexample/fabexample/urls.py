from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'fabexample.views.home', name='home'),
    url(r'^wait$', 'fabexample.views.wait', name='wait'),
    url(r'^admin/', include(admin.site.urls)),
]
