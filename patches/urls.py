from django.conf.urls.defaults import *
from tkldevenv_webapp.patches.views import *

urlpatterns = patterns('',
    ('^$', patches_index),
)
