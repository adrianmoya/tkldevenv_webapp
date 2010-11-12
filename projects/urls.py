from django.conf.urls.defaults import *
from tkldevenv.projects.views import *

urlpatterns = patterns('',
    ('^$', projects_index),
)
