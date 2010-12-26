from django.shortcuts import render_to_response 
from tkldevenv_webapp.utils import list_patches
from tkldevenv_webapp.utils import lastupdated
import os.path

def patches_index(request):
    patches = list_patches();
    patcheslist = []
    for x in patches:
        filename = '/srv/tklpatch/patches/'+x+'/'+x+'.tar.gz'
        if os.path.isfile(filename):
            lastbuilt = lastupdated(filename)
            patcheslist.append({'name': x, 'lastbuilt': lastbuilt})
    return render_to_response("patches/patches.html",{"patcheslist": patcheslist})
