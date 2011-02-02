from django.shortcuts import render_to_response 
from tkldevenv_webapp.utils import list_patches
from tkldevenv_webapp.utils import lastupdated
from django.template import RequestContext
import os, os.path
import datetime
from django import forms
from tkldevenv_webapp.settings import TKLPATCH_PATCHES_ROOT, TKLPATCH_PROJECTS_ROOT
from tkldevenv_webapp.utils import UploadFileForm
from tkldevenv_webapp.utils import handle_upload_file

def patches_index(request):
    patches = list_patches();
    patcheslist = []
    for x in patches:
        filename = '/srv/tklpatch/patches/'+x+'/'+x+'.tar.gz'
        if os.path.isfile(filename):
            lastbuilt = lastupdated(filename)
            patcheslist.append({'name': x, 'lastbuilt': lastbuilt})
        else:
            patcheslist.append({'name':"no consigio "+x})
    return render_to_response("patches/patches.html",{"patcheslist": patcheslist})

def patches_upload(request):
    messages = ""
    if request.method == 'POST':
        form = UploadPatchForm(request.POST, request.FILES)   
        if form.is_valid():
            file = request.FILES['file']
            filename = str(file.name)
            patchname = filename[:-7]
            timestamp = datetime.datetime.now().strftime("%d-%m-%y_%H%M%S")
            patchdir = "%s%s/" % (TKLPATCH_PATCHES_ROOT,patchname)
            versiondir = "%s%s/" % (patchdir, timestamp)
            linkname = "%s%s" % (patchdir, filename)
            linktarget = "%s%s" % (versiondir, filename)
            try:
                if not os.path.exists(patchdir):
                    os.mkdir(patchdir)
                os.mkdir(versiondir)
                handle_upload_file(request.FILES['file'],versiondir)
                if os.path.exists(linkname):
                    os.remove(linkname)
                os.symlink(linktarget, linkname)
            except:
                messages = "There was an error uploading the patch"
                raise
            else:
                messages = "Patch %s uploaded successfully" % (patchname)
    else:
        form = UploadPatchForm()
    return render_to_response("patches/upload.html",{"form": form, "messages": messages}, context_instance=RequestContext(request))


class UploadPatchForm(UploadFileForm):
    def clean_file(self):
        data = self.cleaned_data['file']
        filename = str(data.name)
        if not filename.endswith(".tar.gz"):
            raise forms.ValidationError("The file is not a tar.gz file!")
        return data
