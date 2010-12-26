from django.conf.urls.defaults import *
from tkldevenv-webapp.patches.views import *

urlpatterns = patterns('',
    ('^$', patches_index),
)
