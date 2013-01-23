from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('django.views.generic.simple',
    url(r'^', 'direct_to_template', {'template': 'home.html'}, name='home'),
)
