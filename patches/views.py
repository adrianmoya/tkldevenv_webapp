from django.shortcuts import render_to_response 
from tkldevenv_webapp.utils import list_patches
from tkldevenv_webapp.utils import lastupdated
from tkldevenv_webapp.utils import handle_upload_file
from tkldevenv_webapp.utils import UploadFileForm
from django.template import RequestContext
import os.path
from django import forms
from tkldevenv_webapp.settings import TKLPATCH_PATCHES_ROOT

def patches_index(request):
    patches = list_patches();
    patcheslist = []
    for x in patches:
        filename = '/srv/tklpatch/patches/'+x+'/'+x+'.tar.gz'
        if os.path.isfile(filename):
            lastbuilt = lastupdated(filename)
            patcheslist.append({'name': x, 'lastbuilt': lastbuilt})
    return render_to_response("patches/patches.html",{"patcheslist": patcheslist})

def patches_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)   
        if form.is_valid():
            handle_upload_file(request.FILES['file'], TKLPATCH_PATCHES_ROOT)
    else:
        form = UploadFileForm()
    return render_to_response("patches/upload.html",{"form": form}, context_instance=RequestContext(request))
