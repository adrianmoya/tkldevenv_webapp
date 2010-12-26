from django.conf.urls.defaults import *
from tkldevenv_webapp.projects.views import *

urlpatterns = patterns('',
    ('^$', projects_index),
)
