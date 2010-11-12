from django.conf.urls.defaults import *
from tkldevenv.patches.views import *

urlpatterns = patterns('',
    ('^$', patches_index),
)
