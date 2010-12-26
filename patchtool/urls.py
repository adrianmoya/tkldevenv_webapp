from django.conf.urls.defaults import *
from tkldevenv-webapp.patchtool.views import *

urlpatterns = patterns('',
    ('^$', patchtool_index),
    (r'^apply/$', apply_patch),
    (r'^status/$', status),
)
