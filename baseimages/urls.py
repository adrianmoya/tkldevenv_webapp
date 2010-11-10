from django.conf.urls.defaults import *
from tkldevenv.baseimages.views import *

urlpatterns = patterns('',
    ('^$', baseimages_index),
    (r'^listimages/$', list_images),
    (r'^getimage/$', get_image),
)
