from django.conf.urls.defaults import *
from django.conf import settings
from tkldevenv.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^patchtool/', include('tkldevenv.patchtool.urls')),
    (r'^baseimages/', include('tkldevenv.baseimages.urls')),
    (r'^patches/', include('tkldevenv.patches.urls')),
    (r'^projects/', include('tkldevenv.projects.urls')),
    (r'^output/', include('tkldevenv.output.urls')), 
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^$', main)
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
