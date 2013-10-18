from django.conf.urls.defaults import patterns, url
#from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('celulas.views',
    url(r'^list/(?P<idGrade>\d+)$', 'list', name='list'),
    url(r'^get/(?P<idObj>\d+)/$', 'get', name='get'),
    
    #recebe o id da Grade ->
    url(r'^create/(?P<idGrade>\d+)$', 'create', name='create'),
    
    url(r'^delete/(?P<idObj>\d+)$', 'delete', name='delete'),
    url(r'^avaliar/(?P<idObj>\d+)$', 'avaliar', name='avaliar'),
    url(r'^update/(?P<idObj>\d+)$', 'update', name='update'),
)

