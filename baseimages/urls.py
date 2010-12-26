from django.conf.urls.defaults import *
from tkldevenv_webapp.baseimages.views import *

urlpatterns = patterns('',
    ('^$', images_index),
    (r'^listimages/$', available_images),
    (r'^getimage/$', get_image),
    (r'^refreshfile/$', refresh_list),
)
