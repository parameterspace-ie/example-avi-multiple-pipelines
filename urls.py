'''
GAVIP Example AVIS: Multiple Pipeline AVI

Django URLs and their views
'''

from django.conf.urls import include, patterns, url
from plugins.urls import job_list_urls
from avi import views
    
urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^run_ulysses$', views.run_ulysses, name='run_ulysses'),
    url(r'^run_gacsigsl$', views.run_gacsigsl, name='run_gacsigsl'),
                       
    url(r'^job_list/',
        include(job_list_urls,
        namespace='plugin_job_list')),
    # url(r'^job_list/$', views.job_list, name='job_list'),
                       
    url(r'^result/(?P<job_id>[0-9]+)/$', views.job_result, name='job_result'),
    
    url(r'^help/$', views.help_documentation, name='help'),
)
