from django.conf.urls.defaults import patterns, url
#from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('restricoes.views',
    url(r'^update/(?P<idGrade>\d+)/(?P<idProfessor>\d+)$', 'update', name='update'),
    url(r'^list/(?P<idGrade>\d+)$', 'list', name='list'),
)

