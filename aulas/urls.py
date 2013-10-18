from django.conf.urls.defaults import patterns, url
#from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('aulas.views',
    url(r'^create/(?P<turmaId>\d+)$', 'create', name='create'),
    url(r'^delete/(?P<idObj>\d+)$', 'delete', name='delete'),
    url(r'^update/(?P<idObj>\d+)$', 'update', name='update'),
    url(r'^get_professor_set/$', 'get_professor_set', name='get_professor_set'),
    """                   
    url(r'^$', 'list', name='list'),
    url(r'^get/(?P<idObj>\d+)/$', 'get', name='get'),
    """
)

