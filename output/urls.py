from django.conf.urls.defaults import *
from tkldevenv.output.views import *

urlpatterns = patterns('',
    ('^$', output_index),
    # (r'^getfile/$', get_file),
)
