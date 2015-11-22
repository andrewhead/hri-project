from django.conf.urls import url

import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home$', views.home, name='home'),
    url(r'^queue$', views.queue, name='queue'),
    url(r'^update_vertices$', views.update_vertices, name='update_vertices'),
    url(r'^get_next$', views.get_next, name='get_next'),
]
