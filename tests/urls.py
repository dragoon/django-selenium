from django.conf.urls import patterns, url
from core.views import SampleSearchView


urlpatterns = patterns('',
   url(r'^$', SampleSearchView.as_view(), name='main'),
)
