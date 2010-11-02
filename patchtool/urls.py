from django.conf.urls.defaults import *
from tkldevenv.patchtool.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('^$', patchtool_index),
    (r'^apply/$', apply_patch),
    (r'^status/$', status),
    (r'^listimages/$', list_images),
    (r'^getimage/$', get_image),
)
