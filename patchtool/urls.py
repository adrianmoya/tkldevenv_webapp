from django.conf.urls.defaults import *
from tkldevenv.patchtool.views import *

urlpatterns = patterns('',
    ('^$', patchtool_index),
    (r'^apply/$', apply_patch),
    (r'^status/$', status),
    (r'^listimages/$', list_images),
    (r'^getimage/$', get_image),
)
