from django.conf.urls.defaults import *
from tkldevenv-webapp.projects.views import *

urlpatterns = patterns('',
    ('^$', projects_index),
)
