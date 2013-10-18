from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()


#import grade

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'teste1.views.home', name='home'),
     url(r'^$', 'src.views.home'),
     url(r'^home$', 'src.views.home'),
     
     url(r'^grades/', include('grades.urls', namespace='grades')),
     url(r'^professores/', include('professores.urls', namespace='professores')),
     url(r'^disciplinas/', include('disciplinas.urls', namespace='disciplinas')),
     url(r'^turmas/', include('turmas.urls', namespace='turmas')),
     url(r'^aulas/', include('aulas.urls', namespace='aulas')),
     url(r'^restricoes/', include('restricoes.urls', namespace='restricoes')),
     url(r'^celulas/', include('celulas.urls', namespace='celulas')),
     url(r'^accounts/', include('accounts.urls', namespace='accounts')),
     
    # url(r'^teste1/', include('teste1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
    

    
)
