from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('grades.views',
    url(r'^$', 'list', name='list'),
    url(r'^get/(?P<idObj>\d+)/$', 'get', name='get'),
    url(r'^create/$', 'create', name='create'),
    url(r'^delete/(?P<idObj>\d+)$', 'delete', name='delete'),
    url(r'^update/(?P<idObj>\d+)$', 'update', name='update'),
    url(r'^addTurma/(?P<idObj>\d+)$', 'addTurma', name='addTurma'),
)

