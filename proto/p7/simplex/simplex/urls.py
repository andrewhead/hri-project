from django.conf.urls import url

import simplex.views


urlpatterns = [
    url(r'^$', simplex.views.home, name='home'),
    url(r'^home$', simplex.views.home, name='home'),
    url(r'^update_vertices$', simplex.views.update_vertices, name='update_vertices'),
    url(r'^get_next$', simplex.views.get_next, name='get_next'),
]
